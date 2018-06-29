import os, subprocess

BASE = '''\documentclass [tikz] {{{{standalone}}}}
	\\begin {{document}}
		\\begin {{tikzpicture}} [every node/.style={{{}}}, every edge/.style={{draw, {}}}]
			% Here are the signs commands.
{}
		\\end {{tikzpicture}} 
	\\end
{{document}}'''

OUTFILE="avl.tex"
OUTPDF="avl.pdf"

class Node:
    def __init__(self, num):
        self.key = num
        self.right = None
        self.left = None
        self.p = None
        self.height = 0
        self.factor = 0
        self._find_height()

    def _find_height(self):
        #print("_update: {} ({}, {})".format(self.key, self.factor, self.height))
        r = self.right.height if self.right else -1
        l = self.left.height if self.left else -1

        self.height = max(l, r) + 1
        self.factor = r - l

    def _update_p(self):
        if self.right:
            self.right.p = self

        if self.left:
            self.left.p = self


class AVLTree:

    def __init__(self, num):
        self.root = Node(num)
        self.nodestyle = 'circle, draw'
        self.edgestyle = 'blue, very thick'
        self.command = ''

    def insert(self, key):
        #print("insert: {}".format(key))
        self.root = self._insert(self.root, key)

    def _insert(self, root, key):
        #return a new node if root is None
        if not root:
            return Node(key)


        if key > root.key:
            root.right = self._insert(root.right, key)
            root._find_height()
            if root.right:
                root.right.p = root


        elif key < root.key:
            root.left = self._insert(root.left, key)
            root._find_height()
            if root.left:
                root.left.p = root

        else:
            #key already exists : Do not insert
            pass

        return self._balance(root)

    def _balance(self, root):
        #root._find_height()
        if root:
            if root.factor < -1:
                if root.left.factor <= 0:
                    root = self._ll_rotate(root)
                else:
                    root = self._lr_rotate(root)
            elif root.factor > 1:
                if root.right.factor >= 0:
                    root = self._rr_rotate(root)
                else:
                    root = self._rl_rotate(root)

        return root

    def _ll_rotate(self, root):
        ptr = root.left
        root.left = ptr.right
        root._find_height()
        root._update_p()

        ptr.right = root
        ptr._find_height()
        ptr._update_p()

        return ptr

    def _rr_rotate(self, root):
        ptr = root.right
        root.right = ptr.left
        root._find_height()
        root._update_p()

        ptr.left = root
        ptr._find_height()
        ptr._update_p()

        return ptr

    def _lr_rotate(self, ptr):
        ptr.left = self._rr_rotate(ptr.left)
        ptr._find_height()
        ptr._update_p()

        return self._ll_rotate(ptr)

    def _rl_rotate(self, ptr):
        ptr.right = self._ll_rotate(ptr.right)
        ptr._find_height()
        ptr._update_p()

        return self._rr_rotate(ptr)

    def __str__(self):
        self.command = ''
        self._pre_order(self.root, 0, 0)
        self._find_edges(self.root)
        return BASE.format(self.nodestyle, self.edgestyle, self.command)

    def visualize(self):

        if os.path.isfile(OUTFILE) and os.access(OUTFILE, os.W_OK) == False:
            print('Error: No write permission on file {}. Delete this file & try again!'.format(OUTFILE))
            exit()
        with open(OUTFILE, 'w') as out_file:
            print(self, file=out_file)

        if os.path.isfile(OUTFILE):
            compile_cmd = ["pdflatex", OUTFILE]
            returned_output = subprocess.check_output(compile_cmd)

        if os.path.isfile(OUTPDF):
            show_cmd = ["evince", OUTPDF]
            returned_output = subprocess.check_output(show_cmd)


    #does the pre order traversal of the AVL tree
    def _pre_order(self, ptr, x, y):

        if ptr is not None:
            #print("\\coordinate (x{}) at ({}, {});".format(ptr.key, x, y))
            #print("\\node(n{})at(x{}) {{{}}};".format(ptr.key, ptr.key, ptr.key))
            self.command = self.command + "\t\t\t\\coordinate (x{}) at ({}, {});\n".format(ptr.key, x, y)
            self.command = self.command + "\t\t\t\\node (n{}) at(x{}) {{{}}};\n".format(ptr.key, ptr.key, ptr.key)
            self._pre_order(ptr.left, x-ptr.height-1, y-1)
            self._pre_order(ptr.right, x+ptr.height+1, y-1)


    def _find_edges(self, ptr):
        if ptr is not None:
            if ptr.right is not None:
                #print("\\draw (n{}) edge (n{});".format(ptr.key, ptr.right.key))
                self.command = self.command + "\t\t\t\\draw (n{}) edge (n{});\n".format(ptr.key, ptr.right.key)
                self._find_edges(ptr.right)
            if ptr.left is not None:
                #print("\\draw (n{}) edge (n{});".format(ptr.key, ptr.left.key))
                self.command = self.command + "\t\t\t\\draw (n{}) edge (n{});\n".format(ptr.key, ptr.left.key)
                self._find_edges(ptr.left)





if __name__ == "__main__":
    """
    Execution starts here.
    """
    T = AVLTree(10)
    T.insert(20)
    T.insert(30)
    T.insert(40)
    T.insert(50)
    T.insert(25)
    T.insert(40)
    #T.insert(90)
    print(T)
    T.visualize()
