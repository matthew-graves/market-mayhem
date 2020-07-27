

/////--- Initialization ---/////

$( window ).on( "load", ()=> {
  

///Elements
var canvas = document.getElementById("canvas");
var canvasWidth = canvas.clientWidth;
var canvasHeight = canvas.clientHeight;
var restartButton = document.getElementById("restart-button-div")

///VerletExpressJS
VX.initialize( "2d", "canvas", "canvas", canvasWidth, canvasHeight );
VX.xRange = { min: null, max: null };
VX.yRange = { min: -VX.interfaceHeight*0.2, max: null };
VX.breeze = 1;

///Settings
var beginWithBurst = true;
var confettis = []; var confettiCount = 0;
var confettiVolumeInit = 150;
var confettiVolumeMax = confettiVolumeInit+25;
var confettiWidthMin = VX.interfaceHeight*0.01;
var confettiWidthMax = VX.interfaceHeight*0.015;
var confettiWidth = function() { return VX.rfb( confettiWidthMin, confettiWidthMax );  };
var confettiInitX = function() { return VX.rfb( 0, VX.interfaceWidth ) }; // initial confetti top left corner x position
var confettiInitY = function() { return VX.rfb( -confettiWidthMax, VX.interfaceHeight ) }; // initial confetti top left corner y position
var confettiVelocityBase = confettiWidthMax*0.5;
var initialBurstIntensity = confettiWidthMax*5;
var refreshed = false; 

///colors
var backgroundColor = "#111111";
var confettiAlpha = 1;  // confetti alpha
var janeStreetPalette = [ `rgba( 32, 133, 239, ${confettiAlpha} )`,
                          `rgba( 0, 194, 143, ${confettiAlpha} )`,
                          `rgba( 129, 208, 4, ${confettiAlpha} )`,
                          `rgba( 86, 171, 15, ${confettiAlpha} )` ];
var pastelPartyPalette = [ `rgba( 168, 100, 253, ${confettiAlpha} )`,
                           `rgba( 41, 205, 255, ${confettiAlpha} )`,
                           `rgba( 120, 255, 68, ${confettiAlpha} )`,
                           `rgba( 253, 255, 106, ${confettiAlpha} )`,
                           `rgba( 255, 113, 141, ${confettiAlpha} )` ];
var tropicalSunsetPalette = [ `rgba( 254,218,132, ${confettiAlpha} )`,
                              `rgba( 255,155,131, ${confettiAlpha} )`,
                              `rgba( 151,99,147, ${confettiAlpha} )`,
                              `rgba( 104,84,137, ${confettiAlpha} )`,
                              `rgba( 67,69,127, ${confettiAlpha} )` ];
var goldPalette = [ `rgba( 166,124,0, ${confettiAlpha} )`,
                    `rgba( 191,155,48, ${confettiAlpha} )`,
                    `rgba( 255,191,0, ${confettiAlpha} )`,
                    `rgba( 255,207,64, ${confettiAlpha} )`,
                    `rgba( 255,220,115, ${confettiAlpha} )` ];
var randomPalette = generateRandomPalette(5);
document.getElementById("canvas").style.background = backgroundColor;
var colors = randomPalette;

///Interaction
var mouseCoords = { cx: null, cy: null, px: null, py: null };
var mouseZoneRadius = confettiWidthMax*5;
var mouseStrength = 0.1;
var popperBurstVolumeMax = 50;
var popperBurstIntensity = confettiWidthMax*2;
var popperBurstZoneRadius = confettiWidthMax*10;




/////--- Functions ---/////


function generateRandomPalette( colorCount ) {
  var palette = [];
  for ( var i=0; i<colorCount; i++ ) { 
    palette.push( `rgba( ${VX.rib(0,255)}, ${VX.rib(0,255)}, ${VX.rib(0,255)}, ${confettiAlpha} )` ); 
  }
  return palette
}
  

function Confetti( initX, initY ) {
  confettiCount++;
  this.id = confettiCount;
  this.width = confettiWidth();
  this.color = colors[ VX.rib( 0, colors.length-1 ) ];
  this.pt1 = VX.addPoint( { x: initX, y: initY } );
  this.pt1.px += VX.rfb( -confettiVelocityBase/2, confettiVelocityBase/2 );  // adds initialx velocity
  this.pt1.py += VX.rfb( -confettiVelocityBase, 0 );  // adds initial y velocity
  this.pt2 = VX.addPoint( { x: initX+this.width, y: initY } );
  this.pt3 = VX.addPoint( { x: initX+this.width, y: initY+this.width } );
  this.pt4 = VX.addPoint( { x: initX, y: initY+this.width } );
  this.sp1 = VX.addSpan( this.pt1, this.pt2 );
  this.sp2 = VX.addSpan( this.pt2, this.pt3 );
  this.sp3 = VX.addSpan( this.pt3, this.pt4 );
  this.sp4 = VX.addSpan( this.pt4, this.pt1 );
  this.sp5 = VX.addSpan( this.pt1, this.pt3 );
  this.sk = VX.addSkin( [ this.pt1, this.pt2, this.pt3, this.pt4 ], { fillColor: this.color, outlineColor: "rgba(0,0,0,0)", outlineThickness: 0 } );
}

function runInitialBurst() {  
  for ( var i=0; i<confettiVolumeInit; i++ ) {
    var initAngle = VX.rfb(0,Math.PI*2);
    var initDistance = VX.rfb( 0, VX.interfaceWidth*0.1 );
    var initConfettiX = VX.interfaceWidth*0.5 + Math.cos( initAngle - Math.PI/2 ) * initDistance;
    var initConfettiY = VX.interfaceHeight*0.6 + Math.sin( initAngle - Math.PI/2 ) * initDistance;
    confettis.push( new Confetti( initConfettiX, initConfettiY ) );
    var velocity = VX.rfb( -initialBurstIntensity, initialBurstIntensity );
    var velocityAngle = VX.rfb( 0, Math.PI*2 );
    confettis[confettis.length-1].pt1.px = initConfettiX + Math.cos( velocityAngle-Math.PI/2 ) * velocity;
    confettis[confettis.length-1].pt1.py = initConfettiY + Math.sin( velocityAngle-Math.PI/2 ) * velocity + VX.interfaceWidth*0.01;
  }
}

function runInitialFall() {
  for ( var i=0; i<confettiVolumeInit; i++ ) {
    confettis.push( new Confetti( confettiInitX(), confettiInitY() ) );
  }
  confettiInitY = function() { return -confettiWidthMax*3; };
}

function beginConfetti() {
  beginWithBurst ? runInitialBurst() : runInitialFall();
  confettiInitY = ()=> { return -confettiWidthMax*3; };
  setTimeout( ()=> { refreshed = false }, 1 );
}

function removeConfettiById( id ) {
  for ( var i=0; i<confettis.length; i++ ){ 
    var c = confettis[i]; 
    if ( c.id == id ) { 
      VX.removePoint( c.pt1.id ); VX.removePoint( c.pt2.id ); VX.removePoint( c.pt3.id ); VX.removePoint( c.pt4.id );
      VX.removeSpan( c.sp1.id ); VX.removeSpan( c.sp2.id ); VX.removeSpan( c.sp3.id ); VX.removeSpan( c.sp4.id ); VX.removeSpan( c.sp5.id ); 
      VX.removeSkin( c.sk.id );
      confettis.splice(i,1); 
    }
  }
}

function removeConfettiByIndex( index ) {
  var c = confettis[index];
  VX.removePoint( c.pt1.id ); VX.removePoint( c.pt2.id ); VX.removePoint( c.pt3.id ); VX.removePoint( c.pt4.id );
  VX.removeSpan( c.sp1.id ); VX.removeSpan( c.sp2.id ); VX.removeSpan( c.sp3.id ); VX.removeSpan( c.sp4.id );   
  VX.removeSpan( c.sp5.id ); 
  VX.removeSkin( c.sk.id );
  confettis.splice( index, 1 );
}

function replaceFallenConfettis() {
  for ( var i=0; i<confettis.length; i++ ) {
    var c = confettis[i];  
    if ( c.pt1.cy > VX.interfaceHeight*1.1) {
      removeConfettiById( c.id );
      if ( confettis.length < confettiVolumeInit ) {
        confettis.push( new Confetti( confettiInitX(), confettiInitY() ) );
      }
    }
  }
}

function updateMouseCurrentCoords( event ) { 
  mouseCoords.cx = event.clientX; 
  mouseCoords.cy = event.clientY;
}

function updateMousePreviousCoords() {
  mouseCoords.px = mouseCoords.cx;
  mouseCoords.py = mouseCoords.cy;  
}

function moveConfettisOnMouseOver() {
  for ( var i=0; i<confettis.length; i++ ) {
    var c = confettis[i];
    var xDiff = Math.abs( mouseCoords.cx - c.pt1.cx );
    var yDiff = Math.abs( mouseCoords.cy - c.pt1.cy );
    var mouseVelocityX = mouseCoords.cx - mouseCoords.px;
    var mouseVelocityY = mouseCoords.cy - mouseCoords.py;
    if ( xDiff <= mouseZoneRadius && yDiff <= mouseZoneRadius && mouseCoords.px != null && mouseCoords.py != null ) {
      c.pt1.px -= mouseVelocityX*mouseStrength;
      c.pt1.py -= mouseVelocityY*mouseStrength;
    }
  }
}

function popperBurst( event ) {  
  //blast nearby confettis
  for ( var i=0; i<confettis.length; i++ ) {
    var c = confettis[i];
    var xDiff = c.pt1.cx - mouseCoords.cx;
    var yDiff = c.pt1.cy - mouseCoords.cy;
    var dist = Math.sqrt( Math.abs(xDiff*xDiff) + Math.abs(yDiff*yDiff) );
    var intensity = (popperBurstZoneRadius-dist)*popperBurstIntensity*0.0005;
    if ( dist <= popperBurstZoneRadius ) {
      c.pt1.px = c.pt1.cx - xDiff*intensity;
      c.pt1.py = c.pt1.cy - yDiff*intensity;
    }
  }
  //new confettis burst
  var volume = confettis.length < confettiVolumeMax-popperBurstVolumeMax ? popperBurstVolumeMax : confettiVolumeMax-confettis.length; 
  for ( var i=0; i<volume; i++ ) {
    confettis.push( new Confetti( mouseCoords.cx, mouseCoords.cy ) );
    confettis[confettis.length-1].pt1.px = mouseCoords.cx;
    confettis[confettis.length-1].pt1.py = mouseCoords.cy;
    var velocity = VX.rfb( -popperBurstIntensity, popperBurstIntensity );
    var angle = VX.rfb( 0, Math.PI*2 );
    confettis[confettis.length-1].pt1.px = mouseCoords.cx + Math.cos( angle-Math.PI/2 ) * velocity;
    confettis[confettis.length-1].pt1.py = mouseCoords.cy + Math.sin( angle-Math.PI/2 ) * velocity;
  }
}
  
function refresh() {
  VX.points = [];
  VX.spans = [];
  VX.skins = [];
  confettis = [];
  colors = colors = randomPalette ? generateRandomPalette(5) : colors;
  refreshed = true;
  beginConfetti();
}



/////--- Adapted Functions ---/////

var mv = 5;  // maximum velocity

VX.updatePoints = function() {
  for ( var i=0; i<VX.points.length; i++ ) {
    var p = VX.points[i];
    var xv = ( p.cx - p.px ) * VX.friction;
    var yv = ( p.cy - p.py ) * VX.friction;
    p.px = p.cx;
    p.py = p.cy;
    p.cx += xv; 
    p.cy += yv; 
    p.cy += VX.gravity * p.mass;
    if ( VX.worldTime % VX.rib( 100, 200 ) == 0 ) { p.cx += VX.rfb( -VX.breeze, VX.breeze ); }  
  }
}
    
VX.runOnFrameRefresh = function() { 
  replaceFallenConfettis();
  moveConfettisOnMouseOver();
  updateMousePreviousCoords();
}



/////--- Scaling ---/////
  
function scaleToWindow() {
  VX.interfaceWidth = VX.canvas.width = window.innerWidth;
  VX.interfaceHeight = VX.canvas.height = window.innerHeight;
}

scaleToWindow();


    
/////--- Events ---/////

window.addEventListener( "resize", scaleToWindow );
restartButton.addEventListener( "mousedown", refresh );
document.addEventListener( "mousedown", ()=> { if ( !refreshed ) popperBurst() });
document.addEventListener( "mousemove", updateMouseCurrentCoords );


/////--- Run ---/////

beginConfetti();



});







