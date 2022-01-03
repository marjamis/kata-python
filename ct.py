#!/usr/bin/python2.7

#####################################################################
# Author: Jamis March
# Contact email address: autoproj.dev@gmail.com
#
# Notes: - Requires IAM access to SQS(Full access)
##################################################################### 

import os, time, threading, boto, sys, argparse, boto.sqs, boto.sqs.queue, json, logging, datetime, random

### Start: Functions that make up the API calls to AWS
def CreateQueue():
  global queueRef, sqsconn
  Log('Creating queue...')
  sqsconn = boto.sqs.connect_to_region(args.region)
  queueRef = sqsconn.create_queue(queue_name=args.queuename,
    visibility_timeout='30')
  Log('Created queue: '+args.queuename+' and attributes: ')
  Log(GetQueueAttributes())
    
def DeleteMessage(message, ident):
  Log('Deleting message %s...' % ident)
  sqsconn.delete_message(queueRef, message)
  Log('Deleted message %s.'  % ident)

def DeleteMessageBatch(messages, idents):
  for i in idents:
    Log('Deleting message batch id: %s...' % i)
  sqsconn.delete_message_batch(queueRef, messages)
  for i in idents:
    Log('Deleted message batch id: %s.' % i)
  
def DeleteQueue():
  Log('Deleting queue %s...' % args.queuename)
  sqsconn.delete_queue(queue=queueRef)
  Log('Deleted queue %s.' % args.queuename)

def GetQueueAttributes():
  return sqsconn.get_queue_attributes(queue=queueRef, attribute='All')
  
def ListDeadLetterSourceQueues():
  return sqsconn.get_dead_letter_source_queues(queueRef)
  
def ReceiveMessage():
  return sqsconn.receive_message(queue=queueRef, number_messages=1,
    visibility_timeout=args.vtimeout, attributes='All',
    wait_time_seconds=args.wtimeout, message_attributes='All')
    
def SendMessage(message):
  sqsconn.send_message(queue=queueRef, message_content=message, 
    delay_seconds=0, message_attributes={"Timestamp": {"data_type": "String", 
      "string_value": (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%s'))},
      "Content-Type": {"data_type": "String", "string_value": "application/json"}})
  
def RemainingMessages():
  return sqsconn.get_queue_attributes(queue=queueRef, 
    attribute='ApproximateNumberOfMessages')['ApproximateNumberOfMessages']
  
def SendMessageBatch(messages):
  test = sqsconn.send_message_batch(queue=queueRef, messages=messages)
  print(test)

def ReceiveMessageBatch(numberOfMessages):
  return sqsconn.receive_message(queue=queueRef, 
    number_messages=numberOfMessages,
    visibility_timeout=args.vtimeout, attributes='All',
    wait_time_seconds=args.wtimeout, message_attributes='All')
### End: Functions that make up the API calls to AWS

### Start: Functions that make up the local processing
def LoadCrafting():
  Log('Generating messages to be processed...')
  #First part is for individual messages
  for n in range(0, (args.messages / 2)):
    SendMessage(CreateMessage())
  remaining = args.messages - (args.messages / 2)
      
  #Second part is for batch messages - Doesn't currently work when messageAttributes are set
  run=True
  while ((run==True) & (remaining > 0)):
    listOfMessages = []
    if remaining >= 10:
      number = 10
    else:
      number = remaining
    for k in range(0, number):
      messageAttributes = {'Timestamp': {'data_type': 'String', 
      'string_value': (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%s'))},
      'Content-Type': {'data_type': 'String', 'string_value': 'application/json'}}
      #print messageAttributes
      listOfMessages.append([ k, CreateMessage(), 0, messageAttributes])
    SendMessageBatch(listOfMessages)
    remaining = remaining - len(listOfMessages)

def WorkerProcessing(thread):
  run=True
  while ((run==True) & (queueRef.count() > 0)):
    try:
      message = ReceiveMessage()
      #message = ReceiveMessageBatch(10)
      for i in range(0, len(message)):
        UseMessage(message[i])
        #time.sleep(1)
      Log('Approximate number of remaining messages: %s' % RemainingMessages())
    except IndexError:
      Log('Exception caused by attempted to read a message when there is none')
      run=False    
    except ValueError:
      #Log(json.loads(message[0].get_body()))
      Log('Exception caused by invalid JSON, printing value to see what is being displayed')

def UseMessage(message):
  jsonContent = json.loads(message.get_body())
  Log("Message attributes:")
  Log("Timestamp: %s" % message.message_attributes['Timestamp']['string_value'])
  Log("Content-Type: %s" % message.message_attributes['Content-Type']['string_value'])
  Log(jsonContent['message'])
  DeleteMessage(message, jsonContent['id'])

class myThread(threading.Thread):
  def __init__(self, threadId, name):
    threading.Thread.__init__(self)
    self.threadId = threadId
    self.name = name
  def run(self):
    Log("Starting %s." % self.name)
    WorkerProcessing(self.name)
    Log("Exiting %s." % self.name)
    

def Processing():
  threads=[]
  for i in range(0, args.workers):
    threads.append(myThread(1, "Thread%s" % i))
    threads[i].start()
  
  for t in threads:
    t.join()
  
def CreateMessage():
  return '{\"id\": \"%d\",\"message\": \"%s\"}' % (random.randint(1,1000), 
    ("%d + %d" % (random.randint(1,1000), random.randint(1,1000))))
 
def Log(data):
  print '%s - %s - %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%s'), threading.current_thread(), data)
  output = open('./output.log', 'a')
  output.write('%s - %s - %s\n' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%s'), threading.current_thread(), data))
  output.close()
### End: Functions that make up the local processing

### Start: Create the usage for the allowed arguments
parser = argparse.ArgumentParser(description='Creates and generates messages for an AWS SQS Queue.')
parser.add_argument('-m', '--messages', action='store', type=int, 
  required=True, help='Number of messages to create/run before terminiating.')
parser.add_argument('-w', '--workers', action='store', type=int, 
  required=True, help='Number of workers to process the messages from the queue.')
parser.add_argument('-q', '--queuename', action='store', type=str, 
  default='sqs-queue', help='Name of the queue.')
parser.add_argument('-r', '--region', action='store', type=str,
  default='us-west-2', help='Region to use for the queue.')
parser.add_argument('-vt', '--vtimeout', action='store', type=str,
  default='30', help='Queue and message visibility timeout.')
parser.add_argument('-wt', '--wtimeout', action='store', type=str,
  default='5', 
  help='Time the queue will wait before replying if no available message in the queue.')
parser.add_argument('-l', '--log', action='store', type=str,
  default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
  help='Define the level of log detail, available options: DEBUG, INFO, WARNING, ERROR, CRITICAL.')
args = parser.parse_args()
### End: Create the usage for the allowed arguments

### Start: Configure Python Logging and prints the argument values that will be used
FORMAT="%(levelname)s - %(asctime)s - %(module)s - %(funcName)s - %(message)s"
logging.basicConfig(filename='./module.log', filemode='a', 
  level=args.log.upper(), format=FORMAT)
print 'Values being used: '; print args; print '\n'
### End: Configure Python Logging and prints the argument values that will be used

### Calls the revelant function to complete all workings of this workflow
CreateQueue()
LoadCrafting()

run=True
while(run):
  Processing()
  time.sleep(25)
  if(RemainingMessages() == '0'):
    run=False
Log('All messages processed and printed with %d dead letter source queues' 
  % len(ListDeadLetterSourceQueues()))

DeleteQueue()


