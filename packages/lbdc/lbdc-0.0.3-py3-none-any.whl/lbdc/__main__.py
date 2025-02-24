main = (lambda main : main() if __name__ == "__main__" else main)(lambda a = __import__('sys').argv : open(a[2], 'w').write(λ(open(a[1]).read())))
