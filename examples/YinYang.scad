$fn=1024;


union() {
	difference() {
		union() {
			difference() {
				circle(r = 50);
				translate(v = [-1000, 0]) {
					square(center = true, size = 2000);
				}
			}
			translate(v = [0, 25.0000000000]) {
				circle(r = 25.0000000000);
			}
		}
		translate(v = [0, -25.0000000000]) {
			circle(r = 25.0000000000);
		}
		translate(v = [0, 25.0000000000]) {
			circle(r = 8.3333333333);
		}
	}
	translate(v = [0, -25.0000000000]) {
		circle(r = 8.3333333333);
	}
	difference() {
		circle(r = 52.5000000000);
		circle(r = 50);
	}
}
