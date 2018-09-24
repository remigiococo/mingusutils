from mingusutils import *
import random

def test1():
	rd = randdrum(16, 32, 104)
	rd.set_kit(25)
	#------------------|---|---|---|---
	rd.base_str("bd", "1000100010001000")
	rd.base_str("sn", "0000100000001000")
	rd.base_str("ch", "0010001000100010")
	#
	rd.set_var("ch", [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,
	 1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4])
	rd.gen("testrd1.mid")

def test2():
	rd = randdrum(16, 32, 152)
	rd.set_kit(25)
	#------------------|---|---|---|---
	rd.base_str("bd", "1000000010000000")
	rd.base_str("sn", "0000001000001000")
	rd.base_str("ch", "1011101010111010")
	#rd.base_str("oh", "0010001000100010")
	#
	rd.set_var("ch", [2 for i in xrange(32)])
	rd.gen("testrd2.mid")

def test3():
	rd = randdrum(32, 32, 152, 8)
	rd.set_kit(25)
	#------------------|---|---|---|---|---|---|---|---
	rd.base_str("bd", "10000000000000001000000000000000")
	rd.base_str("sn", "00000000000010000000000010000000")
	rd.base_str("ch", "10001000100010001000100010001000")
	#
	#rd.set_var("ch", [2 for i in xrange(32)])
	rd.gen("testrd3.mid")
	
test1()		
test2()	
test3()	