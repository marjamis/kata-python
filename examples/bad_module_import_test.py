import example_package.bad_module

print('As seen from running, importing this bad module also executes any code outside of a function/class. This can lead to uninttended delays and consequeces. Modules should always have code in a function/method.')
