import subprocess

process = subprocess.call(['mkdir', 'function'], shell=True)
process = subprocess.call(['cd', 'filmbot\\venv\\Lib\\site-packages', '&&',
                           'xcopy', '.', '..\\..\\..\\..\\function', '/S'], shell=True)
process = subprocess.call(['cd', 'filmbot', '&&', 'copy', 'bot.py', '..\\function'], shell=True)
process = subprocess.call(['cd', 'filmbot', '&&', 'copy', 'lb.py', '..\\function'], shell=True)
process = subprocess.call(['cd', 'filmbot', '&&', 'copy', 'tweet_lambda.py', '..\\function'], shell=True)
process = subprocess.call(['cd', 'filmbot', '&&', 'copy', 'poll_lambda.py', '..\\function'], shell=True)
process = subprocess.call(['terraform', 'init'], shell=True)
process = subprocess.call(['terraform', 'apply', '-auto-approve'], shell=True)
process = subprocess.call(['rmdir', '/S', '/Q', 'function'], shell=True)
process = subprocess.call(['del', 'function.zip'], shell=True)


