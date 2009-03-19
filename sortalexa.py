import operator
import csv 

def sort_table(table, cols):
    """ sort a table by multiple columns
        table: a list of lists (or tuple of tuples) where each inner list 
               represents a row
        cols:  a list (or tuple) specifying the column numbers to sort by
               e.g. (1,0) would sort by column 1, then by column 0
    """
    for col in reversed(cols):
        table = sorted(table, key=operator.itemgetter(col))
    return table

if __name__ == '__main__':
	newTop1kReader = csv.reader(open('top-10k-2009-03-19.csv'), delimiter=',')
	oldTop1kReader = csv.reader(open('top-10k-2009-03-06.csv'), delimiter=',')

	newTop1kList = []
	oldTop1kList = []
	
	for row in newTop1kReader:
		newTop1kList += [tuple(row)]
	newTop1kSortedTable = sort_table(tuple(newTop1kList), (1, 0))
	
	for row in oldTop1kReader:
		oldTop1kList += [tuple(row)]
	oldTop1kSortedTable = sort_table(tuple(oldTop1kList), (1, 0))
	

# a   a
#
# c   a - a and b should be ignored
# d   b
# e   c
#
# c   b - c is new
# d   d
#
# a   b
#

	# Now the lists are sorted according to domain name, let's merge them
	# Should deal with that the lists may be of different length
	oldRowIdx = 0
	# I don't know why I would have to do this List/Tuple juggling, I just do it for now
	mergedList = []
	mergedTable = ()
	for newRowIdx in range(0, len(newTop1kSortedTable)):
		newRating, newDN = newTop1kSortedTable[newRowIdx]
		if (oldRowIdx < len(oldTop1kSortedTable)):
			oldRating, oldDN = oldTop1kSortedTable[oldRowIdx]

		while cmp(newDN, oldDN) >= 0 and oldRowIdx < len(oldTop1kSortedTable):
			# If the site names agree, count forward
			if cmp(newDN, oldDN) == 0:
				mergedList += [(newDN, oldRating, newRating)]
				oldRowIdx += 1
				break
			# If the new site... count forward until we find it, but not too far
			else:
				oldRowIdx += 1
				oldRating, oldDN = oldTop1kSortedTable[oldRowIdx]

		# Site is only on the new list
		if cmp(newDN, oldDN) < 0:
			mergedList += [(newDN, '-', newRating)]

	mergedTable = tuple(mergedList)		
	for row in mergedTable:
		print row

	mergedWriter = csv.writer(open('top-10k-2009-03-06-2009-03-19.csv', 'w'), delimiter=",", quotechar='|')
	for row in mergedTable:
		mergedWriter.writerow(row)
