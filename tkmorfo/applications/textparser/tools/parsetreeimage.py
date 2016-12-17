import os
from nltk.tree import Tree
from nltk.draw.tree import TreeView
from tkmorfo.settings import STATICFILES_DIRS

# References 
# http://stackoverflow.com/questions/23429117/saving-nltk-drawn-parse-tree-to-image-file
# http://www.nltk.org/_modules/nltk/tree.html
# http://www.nltk.org/_modules/nltk/draw/tree.html
def save_image_from_tree(raw_tree,name,type='standfor'):
	file_path = STATICFILES_DIRS[0] + '/images/' + type + '/'
	complete_path = file_path + name
	static_path = '/static/images/' + type + '/' + name

	tree = Tree.fromstring(raw_tree)
	TreeView(tree)._cframe.print_to_file(complete_path + '.ps')
	os.system('convert  %s.ps %s.png'% (complete_path,complete_path))
	return static_path + '.png'

