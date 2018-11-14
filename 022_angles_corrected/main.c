/** Include required libraries */ 
#include <math.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include "grid/octree.h" 		// For 3D
#include "view.h"			// For bview
#include "navier-stokes/centered.h"     // Navier stokes 
#include "tracer.h"			// Tracers
#include "diffusion.h"			// Diffusion 

/** Global variables */
int minlevel, maxlevel;         	// Grid depths
double meps, eps;			// Maximum error and error in u fields

char sim_ID[] = "angles";			// Simulation identifier
char sim_var[] = "angles";  		// Notes if a variable is varied over runs

#include "physics.h"			// Physics of the simulation 
#include "fan.h"			// Include a fan
#include "diagnostics.h"		// Perform diagnostics

/** Initialisation */
int main() {	
	minlevel = 3;
  	maxlevel = 9;

   	L0 = 100.;
   	X0 = Y0 = Z0 = 0.;

	// Possibility to run for variable changes
	for(rot.theta = 100.*M_PI/180.; rot.theta<=135.*M_PI/180.; rot.theta+=10.*M_PI/180)
	{
    	init_grid(2<<(6-1));
	a = av; 

	u.x.refine = refine_linear; 			// Momentum conserved 
	u.y.refine = refine_linear;
	#if dimension == 3
		u.z.refine = refine_linear;
	#endif

	fan.prolongation = fraction_refine;		// Fan is a volume fraction
	p.refine = p.prolongation = refine_linear;
	b.gradient = minmod2; 				// Flux limiter 

  	meps = 10.;					// Maximum adaptivity criterion
	DT = 10E-5;					// For poisson solver 
        TOLERANCE=10E-6;				// For poisson solver 
	CFL = 0.5;					// CFL condition

	sim_dir_create();				// Create relevant dir's
	out.sim_i++;					// Simulation iteration 
    	run();						// Start simulation 
	}
}

/** Initialisation */
event init(t = 0){
	rot.rotate = false;
	init_physics();
	init_rotor();
	fan.prolongation=fraction_refine;
	refine (fan[] > 0. && level < maxlevel);
	eps = min(meps, 0.07*rot.cu);
}

/** Return to standard tolerances and DTs for poisson solver */ 
event init_change(i=10){
	TOLERANCE=10E-3;
	DT = 0.05;
}

/** Adaptivity */
event adapt(i++) {
	adapt_wavelet((scalar *){fan,u,b},(double []){0.,eps,eps,eps,1.*9.81/273},maxlevel,minlevel);
}

/** Progress event */
event progress(t+=2.) {
	fprintf(stderr, "i=%d t=%g p=%d u=%d b=%d \n", i, t, mgp.i, mgu.i, mgb.i);
}

event dumpfields(t=30; t+=30) {
	char dumpFile[90];
	snprintf(dumpFile, 90, "%s/dump", out.dir);
	FILE * fpdump = fopen(dumpFile, "w");
	dump(list = all, fp = fpdump);
	fclose(fpdump);
}

/** End the simulation */
event end(t=300.){
}
