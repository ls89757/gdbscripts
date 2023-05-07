# breakpoint at funciton_A if backtracing with function B -> bppf function_A function_B
# show bppf 
# delete bppf [number_in_show]
import gdb
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'
bp_with_passed_function_list = []
def unwind_find_passed_function(passed_function):
	frame = gdb.selected_frame()
	while frame is not None:
		function = frame.function()
		if function is not None:
			function_name = function.name
			#print(function_name)
			is_find = function_name.find(passed_function)
			if is_find != -1:
				return True
			frame = frame.older()
		else:
			#print("Unknown function")
			break
	return False

class bp_with_passed_function(gdb.Breakpoint):
	def __init__(self,break_function, passed_function):
		super().__init__(break_function)
		self.passed_function = passed_function
		self.break_function = break_function
		#self.bp_number = super().number
	def stop(self):
		#return False
	  return unwind_find_passed_function(self.passed_function)
		  
class bp_with_passed_function_command(gdb.Command):
	def __init__(self):
		super(bp_with_passed_function_command,self).__init__("bppf", gdb.COMMAND_USER)
	def invoke(self, argument: str, from_tty: bool) -> None:
		argv = gdb.string_to_argv(argument)
		if len(argv)!=2:
			raise gdb.GdbError("error parameter nums")
		bp_with_passed_function_list.append(bp_with_passed_function(argv[0],argv[1]))

bp_with_passed_function_command()


class show_current_bppf(gdb.Command):
	def __init__(self):
		super(show_current_bppf,self).__init__("show bppf", gdb.COMMAND_USER)
	def invoke(self, argument: str, from_tty: bool) -> None:
		argv = gdb.string_to_argv(argument)
		if len(argv)!=0:
			raise gdb.GdbError("error parameter nums")
		for index,bppf in enumerate(bp_with_passed_function_list):
			print(f'{index}: break at \033[32m{bppf.break_function}\033[0m passed \033[32m{bppf.passed_function}\033[0m')

show_current_bppf()

class delete_a_bppf(gdb.Command):
	def __init__(self):
		super(delete_a_bppf,self).__init__("delete bppf", gdb.COMMAND_USER)
	def invoke(self, argument: str, from_tty: bool) -> None:
		argv = gdb.string_to_argv(argument)
		if len(argv)!=1:
			raise gdb.GdbError("error parameter nums")		
		if argv[0].isnumeric():
			number_in_list = int(argv[0])
			bppf_item = bp_with_passed_function_list[number_in_list] 
			bppf_item.delete()
			bp_with_passed_function_list.remove(bppf_item)
		else:
			raise gdb.GdbError("error bp num")

delete_a_bppf()
# class delete_current_bppf(gdb.Command):
