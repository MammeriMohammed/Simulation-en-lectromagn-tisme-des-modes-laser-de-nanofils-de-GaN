// Gmsh project created on Fri May 24 10:14:03 2024
SetFactory("OpenCASCADE");


/* d_bot, d_sub, d_cov, d_top*/

d_bot = 0.5;
d_top = 0.5;
d_sub = 0.5;
d_cov = 0.5;

x_d = 0;
y_d = ( d_sub + d_bot + d_sub + d_bot + d_cov)/2;
r = 0.1;

/* definition des points pour la région cover*/
Point(1) = { -0.5,d_sub + d_bot + d_cov, 0};
Point(2) = { 0.5, d_sub + d_bot + d_cov, 0};
Point(3) = { 0.5,  d_sub + d_bot , 0};
Point(4) = {-0.5,  d_sub + d_bot , 0}; 

/* les bords de la région cover*/
Line(5) = {1, 2};
Line(6) = {2, 3};
Line(7) = {3, 4};
Line(8) = {4, 1};
//+
Curve Loop(100) = {5, 6, 7, 8};
//+
Plane Surface(101) = {100};

/* definition des points pour la région sub*/
Point(10) = { -0.5, d_sub + d_bot, 0};
Point(11) = { 0.5, d_sub + d_bot , 0};
Point(12) = { 0.5,  d_bot, 0};
Point(13) = {-0.5,  d_bot, 0}; 

/* les bords de la région sub*/
Line(14) = {10, 11};
Line(15) = {11, 12};
Line(16) = {12, 13};
Line(17) = {13, 10};
//+
Curve Loop(200) = {14, 15, 16, 17};
//+
Plane Surface(201) = {200};

/* definition des points pour la région pmlbot*/
Point(20) = { -0.5, d_bot , 0};
Point(21) = { 0.5, d_bot , 0};
Point(22) = { 0.5,  0 , 0};
Point(23) = {-0.5,  0 , 0}; 

/* les bords de la région pmlbot*/
Line(20) = {20, 21};
Line(21) = {21, 22};
Line(22) = {22, 23};
Line(23) = {23, 20};
//+
Curve Loop(300) = {20:23};
//+
Plane Surface(301) = {300};

/* definition des points pour la région pmltop*/
Point(30) = { -0.5, d_sub + d_bot + d_cov + d_top, 0};
Point(31) = { 0.5, d_sub + d_bot + d_cov + d_top, 0};
Point(32) = { 0.5,  d_sub + d_bot + d_cov , 0};
Point(33) = {-0.5,  d_sub + d_bot + d_cov , 0}; 

/* les bords de la région pmltop*/
Line(30) = {30, 31};
Line(31) = {31, 32};
Line(32) = {32, 33};
Line(33) = {33, 30};
//+
Curve Loop(400) = {30:33};
//+
Plane Surface(401) = {400};


Disk(50) = {x_d,y_d,0,r,r};

BooleanDifference{ Surface{101}; Delete; }{ Surface{50};}

Plane Surface(501) = {50};

Physical Surface("cover",1001) = {101};
//+
Physical Surface("nanofil",5001) = {501}; 
//+
Physical Surface("pmlbot", 3001) = {301};
//+
Physical Surface("sub", 2001) = {201};
//+
Physical Surface("pmltop", 4001) = {401};
//+
Mesh 2;


RefineMesh;

// show all merged views
Solver.AutoShowViews = 1;
// don't show last step
Solver.AutoShowLastStep = 0;

// what to do when we double-click on a graph point
PostProcessing.DoubleClickedGraphPointCommand = "OnelabRun('GetDP_NoAutoRun',
  StrCat(Solver.Executable0, ' ', StrPrefix(General.FileName),
         ' -pos plot_boundary plot_h -bin -v 3 ',
         Sprintf('-name res_%g -setnumber ic %g -setnumber selectedEigenvalue %.16g',
                 PostProcessing.DoubleClickedGraphPointX,
                 PostProcessing.DoubleClickedGraphPointX,
                 PostProcessing.DoubleClickedGraphPointY)));
  Draw;";

// macro to convert "h" view from harmonic to time-domain
DefineConstant[
  H2T = {Str["For j In {0:PostProcessing.NbViews-1}",
      "If(!StrCmp(View[j].Name, 'h') || !StrCmp(View[j].Name, 'h_Combine'))",
      "Plugin(HarmonicToTime).View = j;",
      "Plugin(HarmonicToTime).TimeSign = -1;",
      "Plugin(HarmonicToTime).Run;",
      "EndIf",
      "EndFor"],
    Name "}Macros/Convert h-field view to time-domain", AutoCheck 0, Macro "GmshParseString"}
];


















