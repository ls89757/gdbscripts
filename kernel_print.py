# kernel specific print
# p_ino [address of super_block in hex] 
# --->  0: [ino] [address of inode*]
# --->  1: [ino] [address of inode*] 
import gdb
import re

def offsetof(struct_type , member_val_name):
    #ret = gdb.execute("info breakpoints", fa, to_string=True)
    out_str = gdb.execute(f'p &(({struct_type}*)0)->{member_val_name}',False ,to_string=True)
    #print(out_str)
    offset = int(re.search(r'0x([0-9a-fA-F]+)',out_str).group(1),16)
    #offset = int(out_str.split()[-1],16)
    return offset

# 查看一个list所链接的所有struct(或struct中的某一项内容)
# dummy_addr: dummy头结点的地址, gdb.Value()变量，并且类型是struct list_head*
# struct_type: struct类型, str
# list_head_name: list_head 在struct中的名称, str
# member: 若有，则print结构体中该成员，若无则print整个结构体, str
def print_list_head_content(dummy_addr,struct_type, list_head_name, member=None):
    offset = offsetof(struct_type,list_head_name)
    list_head_p = dummy_addr.dereference()['next']
    count = 0
    print(f'=====<{struct_type}*>',end=' ')
    if member:
        for entry in member:
            print(f'{entry}', end=' ')
        print('=====', end='')
    else:
        print('content=====', end='')
    print()

    while list_head_p != dummy_addr:
        void_list_head_p = list_head_p.cast(gdb.lookup_type("void").pointer())
        void_struct_addr = void_list_head_p - offset
        struct_p = void_struct_addr.cast(gdb.lookup_type(struct_type).pointer())
        print(str(count)+":",end=' ')
        if member:
            print(f'{struct_p} ',end=' ')
            for entry in member:
                print(f'{struct_p.dereference()[entry]}',end=' ')
            print()
        else:
            print(f'{struct_p.dereference()}')
        list_head_p = list_head_p.dereference()['next']
        count = count + 1

class print_ino_incache(gdb.Command):
    def __init__(self):
        super(print_ino_incache, self).__init__("p_inode", gdb.COMMAND_USER)
    def invoke(self, argument: str, from_tty: bool) -> None:
        argv = gdb.string_to_argv(argument)
        super_block_addr = gdb.parse_and_eval(argv[0])
        struct_super_block_p = super_block_addr.cast(gdb.lookup_type("struct super_block").pointer())
        s_inodes = struct_super_block_p.dereference()['s_inodes']   
        mem_list = []
        for index in range(1,len(argv)):
            mem_list.append(argv[index])
        print_list_head_content(dummy_addr=s_inodes.address, struct_type="struct inode", list_head_name="i_sb_list", member=mem_list)

print_ino_incache()

class print_sb(gdb.Command):
    def __init__(self):
        super(print_sb, self).__init__("p_sb", gdb.COMMAND_USER)
    def invoke(self, argument: str, from_tty: bool) -> None:
        super_blocks = gdb.parse_and_eval("super_blocks")
        mem_list = ['s_type']
        print_list_head_content(dummy_addr=super_blocks.address, struct_type="struct super_block", list_head_name="s_list", member=mem_list)
print_sb()


class print_sub_dentry(gdb.Command):
    def __init__(self):
        super(print_sub_dentry,self).__init__("p_sub_dentry", gdb.COMMAND_USER)
    def invoke(self, argument: str, from_tty: bool) -> None:
        argv = gdb.string_to_argv(argument)
        parent_dentry_addr = gdb.parse_and_eval(argv[0])
        parent_dentry_p = parent_dentry_addr.cast(gdb.lookup_type("struct dentry").pointer())
        d_subdir = parent_dentry_p.dereference()['d_subdirs']
        mem_list = ["d_iname", "d_inode"]
        print_list_head_content(dummy_addr=d_subdir.address, struct_type="struct dentry", list_head_name= "d_child" , member=mem_list)
print_sub_dentry()
# class print_dentry(gdb.Command):



# class print_inode_cache(gdb.Command):
#     def __init__(self) -> None:
#         super(print_inode_cache, self).__init__("p_ino", gdb.COMMAND_USER)
#     def invoke(self, argument: str, from_tty: bool) -> None:
#         argv = gdb.string_to_argv(argument)
#         if len(argv)!= 1:
#             raise gdb.GdbError("error parameter nums")
#         super_block_addr = gdb.parse_and_eval(argv[0])
#         struct_super_block_p = super_block_addr.cast(gdb.lookup_type("struct super_block").pointer())
#         s_inodes = struct_super_block_p.dereference()['s_inodes']
#         print(s_inodes.address)
#         list_head_p = s_inodes['next']
#         #print(list_head)
#         #offset = 264
#         offset = offsetof("struct inode", "i_sb_list")
#         while list_head_p != s_inodes.address:
#             #print(list_head,end=" ")
#             #print(offset, end= "\n")
#             void_list_head_p = list_head_p.cast(gdb.lookup_type("void").pointer())
#             void_struct_inode_addr = void_list_head_p - offset
#             struct_inode_p = void_struct_inode_addr.cast(gdb.lookup_type("struct inode").pointer())
#             print(list_head_p, end=' ')
#             print(void_struct_inode_addr, end=' ')
#             print(struct_inode_p.dereference()['i_ino'], end="\n")
#             #print(struct_inode_addr, end="\n")
#             list_head_p = list_head_p.dereference()['next']
#             #list_head = list_head['next']
# print_inode_cache()



# class print_super_block(gdb.Command):
#     def __init__(self) -> None:
#         super(print_super_block, self).__init__("p_sb", gdb.Command)
#     def invoke(self, argument: str, from_tty: bool) -> None:


# def lookup_superblock_type():
#     super_blocks = gdb.parse_and_eval("super_blocks")
#     list_head = super_blocks['next']
#     while list_head != super_blocks.address:
#         #print(list_head)
#         super_block_p = list_head.cast(gdb.lookup_type("struct super_block").pointer())
#         print(f'<struct super_block*> {super_block_p}', end="     ")
#         print(super_block_p.dereference()['s_type'].dereference()['name'], end="\n")
#         list_head = list_head['next']

#     type = gdb.lookup_type("struct super_block").pointer()
#       print(type)
