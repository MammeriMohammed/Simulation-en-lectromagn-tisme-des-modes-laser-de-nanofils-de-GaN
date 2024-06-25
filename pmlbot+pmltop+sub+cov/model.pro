Group {
/* region cover */

  c1 = Region[600] ;
  c2 = Region[800] ;
 /*
  c3 = Region[7] ;
  c4 = Region[800] ;
  */
/* region sub   */
  
  c5 = Region[14] ;
  c6 = Region[15] ;
  c7 = Region[16] ;
  c8 = Region[17] ;
  
/* region pmlbot */
  
  c9 = Region[20] ;
  c10 = Region[21] ;
  c11 = Region[22] ;
  c12 = Region[23] ;
  
/* region pmltop */
  
  c13 = Region[30] ;
  c14 = Region[31] ;
  c15 = Region[32] ;
  c16 = Region[33] ;
  
   
  pmltop = Region[4001];
  pmlbot = Region[3001];
  cover = Region[1001];
  sub = Region[2001];
  diel = Region[5001];
  tot = Region[{pmlbot, sub, cover, diel,pmltop}];

  // for visualization of cell boundary 
  /* delimitation des regions physiques*/
  bndGrey = Region[{9998}];
  bndBlack = Region[{9999}];
  bnd = Region[{bndGrey, bndBlack}];
}

Function {
  mu0 = 4.e-7 * Pi ;
  ep0 = 8.854187817e-12 ;
  epsr2[] = Complex[1,0] ; /* l'air*/
  epsr1[] = Complex[2.5,0]; /* diel*/
  a_pml        = 1.;
  b_pml        = 1.;
  sx           = 1.;
  sy[]         = Complex[a_pml,b_pml]; 
  sz           = 1.;
  epsilonr[diel] = epsr2[];
  epsilonr[cover] = epsr2[];
  epsilonr[sub] = epsr1[];
  epsilonr[pmltop] = epsr2[]*sz*sy[]/sx;
  epsilonr[pmlbot] = epsr2[]*sz*sy[]/sx;
  /*
  PML_Tensor[] = TensorDiag[sz*sy[]/sx,sx*sz/sy[],sx*sy[]/sz];
  */
/*  epsilonr[pmltop] = epsr2[] * PML_Tensor[] ;
  epsilonr[pmlbot] = epsr2[] * PML_Tensor[];
  mur[pmltop] = PML_Tensor[];
  mur[pmlbot] = PML_Tensor[];
  */
 /* mur[sub] = TensorDiag[1,1,1];
  mur[cover] = TensorDiag[1,1,1];
  mur[diel] = TensorDiag[1,1,1];
  */

  mur[] = 1.0;
  EZ[] = Vector[0,0,1] ;

  DefineConstant[
    nn = {20, Min 1, Max 100, Step 1, Name "Parameters/1Number of points (N)"},
    ic = {0, Min 0, Max 3*nn-1, Step 1, Loop 1, ReadOnlyRange 1,
      Name "Parameters/1Sol. step (in [0,3N-1])"},
    gam = {2., Choices{0, 1, 2, 4, 2*Pi}, Name "Parameters/1Beta"},
    nmodes = {20, Min 5, Max 100, Step 1, Name "Parameters/1Number of modes"},
    multiplot = {0, Choices{0,1}, Name "Parameters/Plot solution on multiple cells"}
  ];

  /*par1 = KX, par2 = KY*/
  ta = 1;
  dk=1./nn;
  par1 = dk*ic;
  par2 = 0.0;
  dec = 0;
  
  
/*  dk=1./nn;
  ta = 1./Sqrt[3.];
  /* par1 = KY, par2 = KX*/
  If(ic < nn)
    par2 = dk*ic;
    par1 = 0.0;
  EndIf
  If(ic >= nn && ic < 2 * nn)
    par2 = 1.;
    par1 = dk * ta * (ic - nn);
  EndIf
  If (ic >= 2 * nn && ic < 3 * nn)
    par2 = dk * (3 * nn - ic);
    par1 = dk * ta * (3 * nn - ic);
  EndIf

  dec = -0.01;
  If (gam == 0)
    dec = 0.4;
    If (ic < nn / 2)
      dec = -0.5;
    EndIf
    If (ic > 3 * nn - nn / 2)
      dec = -0.5;
    EndIf
    If (ic >= nn / 2 && ic < nn)
      dec=0.2;
    EndIf
    If (ic >= 3 * nn - nn && ic <= 3 * nn - nn / 2)
      dec=0.2;
    EndIf
  EndIf

  Printf("Step %g: parameters %g %g %g %g", ic, par1, par2, gam, dec);

  gamma[] = gam;

  DefineConstant[
    KX = {par1 * 2. * ta * Pi, ReadOnly 1, Name "Parameters/KX",
      Highlight "AliceBlue"},
    KY = {par2 * 2. * ta * Pi, ReadOnly 1, Name "Parameters/KY",
      Highlight "AliceBlue"},
    decalage = {gam * gam / 2.5 + dec, ReadOnly 1, Name "Parameters/Eigensolver shift",
                Help "Target eigenvalue norm for the eigensolver (computed automatically)",
                Highlight "AliceBlue"},
    filter = {1e-4, Name "Parameters/Eigenvalue threshold",
              Help Str["Only store eigenvalue/eigenvector pairs if the real part of the",
                "eigenvalue is larger in absolute value than the given threshold"]},
    // select a single eigenvalue (real part) for post-processing
    selectedEigenvalue = -1
  ];

  // for LinkCplx constraint
  L = 1.;
  s = L/2.; 
  c = 0;
 /* c = Sqrt[3.] * L / 2.;*/
  c13 = Cos[- KX*s - KY*c];
  s13 = Sin[- KX*s - KY*c];
  c24 = Cos[  KX*s - KY*c];
  s24 = Sin[  KX*s - KY*c];
  ca = Cos[KX];
  sa = Sin[KX];
  
  c57 = Cos[- KX*s - KY*c];
  s57 = Sin[- KX*s - KY*c];
  c68 = Cos[  KX*s - KY*c];
  s68 = Sin[  KX*s - KY*c];

  bndCol[bndGrey] = 0;
  bndCol[bndBlack] = Complex[1,1];

  // only store eigenvalues with non-zero real part
  EigFilter[] = (Norm[$EigenvalueReal] > filter);
}

Constraint {
  { Name arete;
    Case {
      { Region c2 ; Type LinkCplx ; RegionRef c1;
        Coefficient  Complex[c13,s13];
	Function Vector[$X+s,$Y+c,0] ;
      }
    /*  { Region c4 ; Type LinkCplx ; RegionRef c2;
        Coefficient  Complex[c24,s24];
	Function Vector[$X-s,$Y+c,0] ;
	
      }
    	{ Region c5 ; Type LinkCplx ; RegionRef c7;
        Coefficient  Complex[c57,s57];
	Function Vector[$X+s,$Y+c,0] ;
      }
      { Region c6 ; Type LinkCplx ; RegionRef c8;
        Coefficient  Complex[c68,s68];
	Function Vector[$X-s,$Y+c,0];
	
    }*/
  }}
  { Name nodal;
    Case {
      { Region c2 ; Type LinkCplx ; RegionRef c1;
        Coefficient  Complex[c13,s13];
	Function Vector[$X+s,$Y+c,0] ;
      }
    /*  { Region c4 ; Type LinkCplx ; RegionRef c2;
        Coefficient  Complex[c24,s24];
	Function Vector[$X-s,$Y+c,0] ;
      }
      
      { Region c5 ; Type LinkCplx ; RegionRef c7;
        Coefficient  Complex[c57,s57];
	Function Vector[$X+s,$Y+c,0] ;
      }
      { Region c6 ; Type LinkCplx ; RegionRef c8;
        Coefficient  Complex[c68,s68];
	Function Vector[$X-s,$Y+c,0];
	
      }*/
    }
  }
}

FunctionSpace {
  { Name H_nodal; Type Form0;
    BasisFunction {
      { Name sn; NameOfCoef hn; Function BF_Node;
        Support tot; Entity NodesOf[All]; }
    }
    Constraint {
      { NameOfCoef hn; EntityType NodesOf ; NameOfConstraint nodal; }
    }
  }

  { Name H_arete; Type Form1;
    BasisFunction {
      { Name se; NameOfCoef he; Function BF_Edge;
        Support tot; Entity EdgesOf[All]; }
    }
    Constraint {
      { NameOfCoef he; EntityType EdgesOf ; NameOfConstraint arete; }
    }
  }

  /*{ Name H_arete_perp; Type Form1P;
    BasisFunction {
      { Name sn; NameOfCoef hn; Function BF_PerpendicularEdge;
        Support tot; Entity NodesOf[All]; }
    }
    Constraint {
      { NameOfCoef hn; EntityType NodesOf ; NameOfConstraint nodal; }
    }
  }

  { Name H_facet_perp; Type Form2;
    BasisFunction {
      { Name sn; NameOfCoef hn; Function BF_PerpendicularFacet;
        Support tot; Entity EdgesOf[All]; }
    }
  }*/
}

Jacobian{
  { Name JVol ;
    Case {
      { Region All ; Jacobian Vol ; }
    }
  }
}

Integration {
  { Name I1 ;
    Case {
      { Type Gauss ;
        Case {
          { GeoElement Triangle ; NumberOfPoints 3 ; }
        }
      }
    }
  }
}

Formulation {
  // H-formulation in conical incidence
  { Name Guide_h_2D; Type FemEquation;
    Quantity {
      { Name Ht; Type Local; NameOfSpace H_arete; }
      { Name Hl; Type Local; NameOfSpace H_arete_perp; }
    }
    Equation {
      Galerkin { [ 1/mur[] * Dof{d Ht} , {d Ht} ];
        In tot; Integration I1; Jacobian JVol; }
      Galerkin { [ 1/mur[] * Dof{d Hl} , {d Hl} ];
        In tot; Integration I1; Jacobian JVol; }
      Galerkin { DtDtDof [ epsilonr[] * Dof{Ht} , {Ht} ];
        In tot; Integration I1; Jacobian JVol; }
      Galerkin { DtDtDof [ epsilonr[] * Dof{Hl} , {Hl} ];
        In tot; Integration I1; Jacobian JVol; }

      Galerkin { [ - Complex[0,gamma[]]/mur[] * (EZ[] /\ Dof{Ht}) , {d Hl} ];
        In tot; Integration I1; Jacobian JVol; }
      Galerkin { [ Complex[0,gamma[]]/mur[] * Dof{d Hl} ,  EZ[] /\ {Ht} ];
        In tot; Integration I1; Jacobian JVol; }
      Galerkin { [ gamma[]^2/mur[] * (EZ[] /\ Dof{Ht}) , EZ[] /\ {Ht} ];
        In tot; Integration I1; Jacobian JVol; }
    }
  }
}

Resolution {
  { Name Guide_h_2D_PVP;
    System {
      { Name A; NameOfFormulation Guide_h_2D; Type Complex; }
    }
    Operation {
      CreateDir["res"] ;
      GenerateSeparate[A];
      EigenSolve[A, nmodes, decalage, 0, EigFilter[]];
      SaveSolutions[A] ;
      RenameFile["model.pre", Sprintf("model_%g.pre", ic)];
      RenameFile["model.res", Sprintf("model_%g.res", ic)];
      PostOperation[plot_step] ;
    }
  }
}

PostProcessing {
  { Name Guide_h_2D; NameOfFormulation Guide_h_2D; NameOfSystem A;
    Quantity {
      { Name step;     Value { Local { [ ic ]; In tot ; Jacobian JVol; } } }

      { Name boundary; Value { Local { [ bndCol[] ] ; In bnd ; Jacobian JVol ; } } }

      { Name h; Value{ Local{ [ {Ht}+{Hl} ]; In tot; Jacobian JVol; } } }
      { Name hb;      Value { Local { [ ({Ht}+{Hl})* Complex[c13,-s13]                      ]; In tot; Jacobian JVol; } } }
      { Name ha;      Value { Local { [ ({Ht}+{Hl})* Complex[ca, sa ]                       ]; In tot; Jacobian JVol; } } }
      { Name hb1_a;   Value { Local { [ ({Ht}+{Hl})* Complex[c13, s13] * Complex[ca, sa]    ]; In tot; Jacobian JVol; } } }
      { Name hb_a;    Value { Local { [ ({Ht}+{Hl})* Complex[c13,-s13] * Complex[ca, sa]    ]; In tot; Jacobian JVol; } } }
      { Name h2a;     Value { Local { [ ({Ht}+{Hl})* Complex[ca, sa]^2                      ]; In tot; Jacobian JVol; } } }
      { Name hb1_2a;  Value { Local { [ ({Ht}+{Hl})* Complex[c13, s13] * Complex[ca, sa]^2  ]; In tot; Jacobian JVol; } } }
      { Name h2b;     Value { Local { [ ({Ht}+{Hl})* Complex[c13,-s13]^2                    ]; In tot; Jacobian JVol; } } }
      { Name h2b1_2a; Value { Local { [ ({Ht}+{Hl})* Complex[c13, s13]^2 * Complex[ca, sa]^2]; In tot; Jacobian JVol; } } }

      { Name ht;       Value { Local { [ {Ht}                                         ]; In tot; Jacobian JVol; } } }
      { Name htb;      Value { Local { [ {Ht}* Complex[c13,-s13]                      ]; In tot; Jacobian JVol; } } }
      { Name hta;      Value { Local { [ {Ht}* Complex[ca, sa ]                       ]; In tot; Jacobian JVol; } } }
      { Name htb1_a;   Value { Local { [ {Ht}* Complex[c13, s13] * Complex[ca, sa]    ]; In tot; Jacobian JVol; } } }
      { Name htb_a;    Value { Local { [ {Ht}* Complex[c13,-s13] * Complex[ca, sa]    ]; In tot; Jacobian JVol; } } }
      { Name ht2a;     Value { Local { [ {Ht}* Complex[ca, sa]^2                      ]; In tot; Jacobian JVol; } } }
      { Name htb1_2a;  Value { Local { [ {Ht}* Complex[c13, s13] * Complex[ca, sa]^2  ]; In tot; Jacobian JVol; } } }
      { Name ht2b;     Value { Local { [ {Ht}* Complex[c13,-s13]^2                    ]; In tot; Jacobian JVol; } } }
      { Name ht2b1_2a; Value { Local { [ {Ht}* Complex[c13, s13]^2 * Complex[ca, sa]^2]; In tot; Jacobian JVol; } } }

      { Name hlz;       Value { Local { [ CompZ[{Hl}                                         ] ]; In tot; Jacobian JVol; } } }
      { Name hlzb;      Value { Local { [ CompZ[{Hl}* Complex[c13,-s13]                      ] ]; In tot; Jacobian JVol; } } }
      { Name hlza;      Value { Local { [ CompZ[{Hl}* Complex[ca, sa ]                       ] ]; In tot; Jacobian JVol; } } }
      { Name hlzb1_a;   Value { Local { [ CompZ[{Hl}* Complex[c13, s13] * Complex[ca, sa]    ] ]; In tot; Jacobian JVol; } } }
      { Name hlzb_a;    Value { Local { [ CompZ[{Hl}* Complex[c13,-s13] * Complex[ca, sa]    ] ]; In tot; Jacobian JVol; } } }
      { Name hlz2a;     Value { Local { [ CompZ[{Hl}* Complex[ca, sa]^2                      ] ]; In tot; Jacobian JVol; } } }
      { Name hlzb1_2a;  Value { Local { [ CompZ[{Hl}* Complex[c13, s13] * Complex[ca, sa]^2  ] ]; In tot; Jacobian JVol; } } }
      { Name hlz2b;     Value { Local { [ CompZ[{Hl}* Complex[c13,-s13]^2                    ] ]; In tot; Jacobian JVol; } } }
      { Name hlz2b1_2a; Value { Local { [ CompZ[{Hl}* Complex[c13, s13]^2 * Complex[ca, sa]^2] ]; In tot; Jacobian JVol; } } }
    }
  }
}

PostOperation {
  { Name plot_step; NameOfPostProcessing Guide_h_2D;
    Operation {
      Print[ step, OnPoint{0,0,0}, Format ValueOnly, File "res/step.txt", SendToServer "GetDP/Step"{0} ] ;
    }
  }

  { Name plot_h; NameOfPostProcessing Guide_h_2D;
    If(selectedEigenvalue >= 0)
      TimeValue selectedEigenvalue;
    EndIf
    Operation {
      Echo[ Str["For i In {PostProcessing.NbViews-1:0:-1}",
                "   If(!StrCmp(View[i].Name, 'h') || !StrCmp(View[i].Name, 'h_Combine'))",
                "     Delete View[i];",
                "   EndIf",
                "EndFor"], File "res/tmp1.geo", LastTimeStepOnly] ;
      Print[ h, OnElementsOf tot, File Sprintf("res/h1_%g.pos", ic) ] ;
      If(multiplot)
        Print[ hb,      OnElementsOf tot, File Sprintf("res/h2_%g.pos", ic), ChangeOfCoordinates {$X+s,$Y+c,$Z}, Name "h" ] ;
        Print[ ha,      OnElementsOf tot, File Sprintf("res/h3_%g.pos", ic), ChangeOfCoordinates {$X+1,$Y,$Z}, Name "h" ] ;
        Print[ hb1_a,   OnElementsOf tot, File Sprintf("res/h4_%g.pos", ic), ChangeOfCoordinates {$X+1-s,$Y-c,$Z}, Name "h" ] ;
        Print[ hb_a,    OnElementsOf tot, File Sprintf("res/h5_%g.pos", ic), ChangeOfCoordinates {$X+1+s,$Y+c,$Z}, Name "h" ] ;
        Print[ h2a,     OnElementsOf tot, File Sprintf("res/h6_%g.pos", ic), ChangeOfCoordinates {$X+2,$Y,$Z}, Name "h" ] ;
        Print[ hb1_2a,  OnElementsOf tot, File Sprintf("res/h7_%g.pos", ic), ChangeOfCoordinates {$X+2-s,$Y-c,$Z}, Name "h" ] ;
        Print[ h2b,     OnElementsOf tot, File Sprintf("res/h8_%g.pos", ic), ChangeOfCoordinates {$X+2*s,$Y+2*c,$Z}, Name "h" ] ;
        Print[ h2b1_2a, OnElementsOf tot, File Sprintf("res/h9_%g.pos", ic), ChangeOfCoordinates {$X+2-2*s,$Y-2*c,$Z}, Name "h" ] ;
        Echo[ "Combine ElementsByViewName;", File "res/tmp2.geo", LastTimeStepOnly] ;
      EndIf
    }
  }

  { Name plot_boundary; NameOfPostProcessing Guide_h_2D; LastTimeStepOnly;
    Operation {
      Echo[ Str["For i In {PostProcessing.NbViews-1:0:-1}",
                "  If(!StrCmp(View[i].Name, 'boundary') || !StrCmp(View[i].Name, 'boundary_Combine'))",
                "    Delete View[i];",
                "  EndIf",
                "EndFor"], File "res/tmp1.geo"] ;
      Print[ boundary, OnElementsOf bnd, File "res/boundary1.pos"];
      If(multiplot)
        Print[ boundary, OnElementsOf bnd, File "res/boundary2.pos",  ChangeOfCoordinates {$X+s,$Y+c,$Z} ] ;
        Print[ boundary, OnElementsOf bnd, File "res/boundary3.pos", ChangeOfCoordinates {$X+1,$Y,$Z} ] ;
        Print[ boundary, OnElementsOf bnd, File "res/boundary4.pos", ChangeOfCoordinates {$X+1-s,$Y-c,$Z} ] ;
        Print[ boundary, OnElementsOf bnd, File "res/boundary5.pos", ChangeOfCoordinates {$X+1+s,$Y+c,$Z} ] ;
        Print[ boundary, OnElementsOf bnd, File "res/boundary6.pos", ChangeOfCoordinates {$X+2,$Y,$Z} ] ;
        Print[ boundary, OnElementsOf bnd, File "res/boundary7.pos", ChangeOfCoordinates {$X+2-s,$Y-c,$Z} ] ;
        Print[ boundary, OnElementsOf bnd, File "res/boundary8.pos", ChangeOfCoordinates {$X+2*s,$Y+2*c,$Z} ] ;
        Print[ boundary, OnElementsOf bnd, File "res/boundary9.pos", ChangeOfCoordinates {$X+2-2*s,$Y-2*c,$Z} ];
        Echo[ "Combine ElementsByViewName;", File "res/tmp2.geo" ] ;
      EndIf
      Echo[ Str["l=PostProcessing.NbViews-1; View[l].ColorTable={Grey80,Black}; ",
                "View[l].ShowScale=0; View[l].LineWidth=2; View[l].LineType=1;"],
            File "res/tmp3.geo" ] ;
    }
  }
}

DefineConstant[
  // always solve this resolution (it's the only one provided)
  R_ = {"Guide_h_2D_PVP", Name "GetDP/1ResolutionChoices", Visible 0},

  // set some command-line options for getdp
  C_ = {"-solve -slepc -bin", Name "GetDP/9ComputeCommand", Visible 0},

  // don't do the post-processing pass
  P_ = {"", Name "GetDP/2PostOperationChoices", Visible 0},

  // plot real part of eigenvalues in terms of step (GetDP/Step is created in
  // post-processing in order to get the correct number of abscissa values --
  // which depends on the number of eigenvalues we compute)
  omega_ = {0, Name "GetDP/Re(Omega)", ReadOnly 1, Graph "01"},
  step_ = {0, Name "GetDP/Step", ReadOnly 1, Graph "10", Visible 0}
];
