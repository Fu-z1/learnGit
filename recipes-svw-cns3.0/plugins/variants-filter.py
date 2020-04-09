import sys
import re

def filterVariant(args, **kwargs):
  '''
  # Parameters
  # arg[0]: string, comma seperated list of variants/regular expressions
  # arg[1]: string, current variant
  '''
  if ',' in args[0]:
    listOfVariants = args[0].split(',')
  else:
    if len(args[0]) > 0:
      listOfVariants = [args[0]]
    else:
      listOfVariants = []

  if args[1] in listOfVariants:
    return 'True'

  for var in listOfVariants:
    if re.search(var, args[1]):
      return 'True'

  return 'False'

manifest = {
    'apiVersion' : "0.2",
    'stringFunctions' : {
        'filterVariant' : filterVariant
    }
}
