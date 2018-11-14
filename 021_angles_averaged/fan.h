#include "fractions.h"	// Needed to compute fan fractions

struct sRotor rot;  		// Rotor details structure 
scalar fan[];			// Fan volume fraction

struct sRotor {	
	double rampT;		// Time to start up rotor
	double P, Prho;		// Power, powerdensity 
	double R, W, A, V;	// Diameter, Thickness, Area ,Volume
	double diaVol;		// Diagnosed rotor volume 
	double x0, y0, z0;	// Origin of rotor
    	double xt, yt, zt;      // Translation angles
	double theta, phi;	// Polar and Azimuthal angle 
   	double thetat, phit;    // Translation angles 
   	double Work;            // Work done by rotor
   	double cu;              // Characteristic velocity
   	bool rotate;            // Rotation yes or no
	coord nf, nr;		// Normal vector fan, rotation 
};

/** Functions */
void init_rotor();
void rotor_update();
void rotor_coord();
void rotor_forcing();

/** Function returning the sRotor structure, includign default properties */
void init_rotor() {
	rot.Work = 0.;
    	if(!rot.rampT)
	    	rot.rampT = 1.;
    	if(!rot.R)
	    	rot.R = L0/80.;     
    	if(!rot.W)
	    	rot.W = 0.3;    
    	if(!rot.Prho)                  
     		rot.Prho = 8.*L0;		
   	if(!rot.x0)
    		rot.x0 = L0/2.;
    	if(!rot.y0)
	    	rot.y0 = L0/2.;
    	if(!rot.z0){
        #if dimension == 2
            	rot.z0 = 0.;
        #elif dimension == 3
            	rot.z0 = L0/2.;
        #endif
        }
    	if(!rot.theta)
	    	rot.theta = 100*M_PI/180.;		// Polar angle
    	if(!rot.phi)
	    	rot.phi = 0.*M_PI/180.;		// Azimuthal angle 

    	if(rot.rotate) {
        	rot.xt = 0;
        	rot.yt = 0;
        	rot.zt = 0;
        	rot.thetat = 0.;
       	 	rot.phit = -0.2*M_PI/180.;
    	} else {
       		rot.xt = 0;
        	rot.yt = 0;
        	rot.zt = 0;
        	rot.thetat = 0.;
        	rot.phit = 0.;
    }
	rotor_update();
}

/** Forcing by the rotor */
event forcing(i = 1; i++) {
	rotor_coord();
	rotor_forcing();
}

/** Rotate the rotor */
event rotate(t+=0.1) {
    if(rot.rotate) { 
        // Change center  
        rot.x0 += rot.xt;
        rot.y0 += rot.yt;
        rot.z0 += rot.zt;

        // Change angles 
        rot.theta += rot.thetat;
        rot.phi += rot.phit;

        rotor_update();
    }
}

/** Updating relevant rotor variables */
void rotor_update() {
   
    	rot.nf.x = sin(rot.theta)*cos(rot.phi);
	rot.nf.z = sin(rot.theta)*sin(rot.phi);
	rot.nf.y = cos(rot.theta);

	rot.nr.x = sin(rot.theta)*cos(rot.phi);
   	rot.nr.z = sin(rot.theta)*sin(rot.phi);
    	rot.nr.y = cos(rot.theta);

   	#if dimension == 2	
		rot.A = 2*rot.R*rot.W;
	#elif dimension == 3    	
		rot.A = sq(rot.R)*M_PI;      
	#endif

        // Volume is slice of a sphere
  	#if dimension == 2
		rot.V = 1.*rot.A;
	#elif dimension == 3 
		rot.V = 4.*M_PI*pow(rot.R,3.)/3. - 
			2*M_PI*pow(rot.R-rot.W/2., 2.)/3.*(2*rot.R + rot.W/2.);
	#endif

	rot.P = rot.V*rot.Prho;
    	rot.cu = pow(3*rot.Prho*rot.W*crho, 1./3.);
}

/** Function returning the volume fractions of a fan object */
void rotor_coord() {

    	scalar sph[], plnu[], plnd[];
   	fraction(sph, -sq((x - rot.x0)) - sq((y - rot.y0)) - sq((z - rot.z0)) + sq(rot.R));
  	fraction(plnu,  rot.nr.x*(x - rot.x0) + rot.nr.y*(y - rot.y0) + rot.nr.z*(z - rot.z0) + rot.W/2.);
   	fraction(plnd, -rot.nr.x*(x - rot.x0) - rot.nr.y*(y - rot.y0) - rot.nr.z*(z - rot.z0) + rot.W/2.);	

	foreach () {
    		fan[] = sph[]*plnu[]*plnd[];
   	}
	boundary({fan});
}

/** Function returning new velocities based on a rotor forcing.
This is a function of powerdensity, width, direction, ramp-time, and diagnosed volume */
void rotor_forcing(){
	double tempW = 0.;
	double w, wsgn, damp, usgn, utemp, corrP;
	foreach(reduction(+:tempW)) {		
		if(fan[] > 0.) {
			foreach_dimension() {
			// Work in respective direction 
			wsgn = sign(rot.nf.x*u.x[]) + (sign(rot.nf.x*u.x[]) == 0)*sign(rot.nf.x);
			damp = rot.rampT > t ? t/rot.rampT : 1.;
			corrP = rot.diaVol > 0. ? rot.V/rot.diaVol : 1.;
			w = wsgn*fan[]*damp*sq(rot.nf.x)*(2./rho[])*(corrP*rot.P/rot.V)*dt;
			tempW += 0.5*rho[]*w*dv();

			// New kinetic energy
			utemp = sq(u.x[]) + w;

			usgn = 	  1.*(u.x[] >= 0)*(utemp > 0) +
			    	 -1.*(u.x[] >= 0)*(utemp < 0) +
		 		  1.*(u.x[] <  0)*(utemp < 0) +
				 -1.*(u.x[] <  0)*(utemp > 0); 

			u.x[] = usgn*sqrt(fabs(utemp));
		}
		}
	}
	rot.Work += tempW;
}
