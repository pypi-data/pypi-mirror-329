



union() {
	union() {
		import(file = "one/two/three/simple_cylinder-10,5.stl", origin = [0, 0]);
		cylinder(h = 10, r = 5);
	}
	rotate(a = 180, v = [1, 0, 0]) {
		union() {
			import(file = "one/two/three/simple_cylinder-10,5.stl", origin = [0, 0]);
			cylinder(h = 10, r = 5);
		}
	}
}
