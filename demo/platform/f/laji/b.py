import a
class B(a.A):
	def out(self):
		print "b"

b = B()
b.process()
