#include "SGS.h"
#define INVERSION .1 				// Kelvin per meter
#define strat(s) 9.81*(INVERSION + 9.81/1005)*s/273.

double crho = 1.;
scalar b[];		
scalar * tracers = {b};
face vector av[]; 
struct sCase def;

struct sCase {
	double ugeo;
	double vgeo;
	double corf;
};

void init_physics(){
        u.n[bottom] = dirichlet(0.);
	u.t[bottom] = dirichlet(0.);
	u.r[bottom] = dirichlet(0.);
	u.n[top] = dirichlet(0.);
	u.t[top] = dirichlet(def.ugeo);
	u.r[top] = dirichlet(def.vgeo);

	b[bottom] = neumann(0.);
	b[top] = neumann(0.);

	def.ugeo = 0.;
	def.vgeo = 0.;
	def.corf = pow(10.,-4.);
	b.nodump = true; 
    	
	periodic (left);
	#if dimension == 3
		periodic(front);
	#endif  

	foreach() {
		b[] = strat(y);
		u.x[] = 1.*def.ugeo;
		u.z[] = 1.*def.vgeo;
	}
}

/* Gravity forcing */
event acceleration(i++){
	foreach_face(y){
		av.y[] = (b[] + b[0,-1])/2.;
	}
	if(def.ugeo>0.){
		foreach_face(x){
			av.x[] = (def.ugeo - uf.x[])*def.corf;
		}
	}
	if(def.vgeo>0.){
		foreach_face(z){
			av.z[] = (def.vgeo - uf.z[])*def.corf;
		}
	} 
}

mgstats mgb;

/* Diffusion */
event tracer_diffusion(i++){
	mgb = diffusion(b, dt, mu);
}
