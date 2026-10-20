$title ERCOT 365-Day Net Renewable Generation & Dispatch Optimization

Sets
    d 'Days of the year (365 days)' / d1*d365 /
    g 'Thermal units'               / g1*g5 /;

Parameters
    TotalLoad(d)  'Total ERCOT Load (MW)'
    WindCap(d)    'Available Wind Generation (MW)'
    SolarCap(d)   'Available Solar Generation (MW)';

* --- 1. 365-DAY ANNUAL PROFILE INITIALIZATION ---
loop(d,
    TotalLoad(d) = 43000 + 4000 * sin(ord(d) * 2 * pi / 365) + 1500 * cos(ord(d) * 4 * pi / 365);
    WindCap(d)   = 14.0  + 4.5  * cos(ord(d) * 2 * pi / 365);
    SolarCap(d)  = 26.0  + 9.0  * sin(ord(d) * 2 * pi / 365);
);

* --- 2. GENERATOR PARAMETERS ---
Parameters
    Pmin(g)  'Thermal unit minimum limits (MW)'   / g1 30, g2 25, g3 15, g4 10, g5 10 /
    Pmax(g)  'Thermal unit maximum limits (MW)'   / g1 200, g2 150, g3 100, g4 70, g5 40 /
    b(g)     'Thermal marginal cost ($/MWh)'      / g1 18, g2 28, g3 35, g4 18, g5 25 /
    
    CurtailPenalty 'Curtailment penalty cost ($/MWh)' / 50.0 /;

Variables
    Z                 'Total annual system operating cost ($)'
    P_thermal(g,d)    'Thermal generation (MW)'
    P_wind(d)         'Optimized Wind generation (MW)'
    P_solar(d)        'Optimized Solar generation (MW)'
    Curtail_wind(d)   'Wind curtailment (MW)'
    Curtail_solar(d)  'Solar curtailment (MW)';

* --- 3. VARIABLE BOUNDS ---
P_thermal.lo(g,d) = Pmin(g);
P_thermal.up(g,d) = Pmax(g);

P_wind.lo(d)  = 0;
P_wind.up(d)  = WindCap(d);

P_solar.lo(d) = 0;
P_solar.up(d) = SolarCap(d);

Equations
    cost_obj             'Objective function with curtailment penalties'
    power_balance(d)     'Overall system power balance'
    wind_curtail_calc(d) 'Wind curtailment tracking'
    solar_curtail_calc(d)'Solar curtailment tracking';

* --- 4. EQUATION DEFINITIONS ---
cost_obj..
    Z =E= sum((g,d), b(g) * P_thermal(g,d)) 
        + sum(d, CurtailPenalty * (Curtail_wind(d) + Curtail_solar(d)));

power_balance(d)..
    sum(g, P_thermal(g,d)) + P_wind(d) + P_solar(d) =E= TotalLoad(d);

wind_curtail_calc(d)..
    Curtail_wind(d) =E= WindCap(d) - P_wind(d);

solar_curtail_calc(d)..
    Curtail_solar(d) =E= SolarCap(d) - P_solar(d);

* --- 5. SOLVE MODEL USING CBC ---
Model ercot_renewable_opt / all /;
Option lp = cbc;
Option reslim = 300;

Solve ercot_renewable_opt using lp minimizing Z;

* --- 6. DISPLAY & CSV EXPORT (Using v2 filename to avoid file locks) ---
Display P_wind.l, P_solar.l, Curtail_wind.l, Curtail_solar.l, Z.l;

File results / ercot_365day_results_v2.csv /;
results.pw = 32767;
put results;
put "Day,TotalLoad,WindAvail,WindDispatched,WindCurtail,SolarAvail,SolarDispatched,SolarCurtail" /;
loop(d,
    put d.tl:0, ",", TotalLoad(d):0:2, ",", WindCap(d):0:2, ",", P_wind.l(d):0:2, ",", Curtail_wind.l(d):0:2, ",", SolarCap(d):0:2, ",", P_solar.l(d):0:2, ",", Curtail_solar.l(d):0:2 /;
);
putclose results;