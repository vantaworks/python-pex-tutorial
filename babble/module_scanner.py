from pip_module_scanner.scanner import Scanner, ScannerException

try:
   scanner = Scanner(path="babble/")
   scanner.run()
   
   # do whatever you want with the results here
   # example:
   for lib in scanner.libraries_found:
       print ("Found module %s at version %s" % (lib.key, lib.version))
   
except ScannerException as e:
    print("Error: %s" % str(e))