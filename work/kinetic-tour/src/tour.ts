export type ZoneId = 'home' | 'motion' | 'clinical' | 'engineering' | 'projects';
export type Point = [number, number, number];
export interface Zone {
  id: ZoneId; number: string; title: string; description: string;
  position: Point; target: Point; image: string;
  details: [string, string][];
}
// Coordinates are glTF Y-up: Blender (x,y,z) becomes (x,z,-y).
export const zones: Zone[] = [
  {id:'home', number:'00 / OVERVIEW', title:'Ideas take<br><em>shape here.</em>',
    description:'Four connected disciplines. One shared workspace. A studio built around movement, investigation, and making.',
    position:[0,3.05,15.2],target:[0,2.1,-2.3],image:'home',
    details:[['The shared center','A walnut workstation connects the four disciplines, with adjustable seating, task lighting and organized cables.'],['Material language','Walnut, graphite, woven fabric and brushed metal share a warm, restrained palette.'],['At blue hour','Warm task lighting meets a cool, artist-authored alpine exterior.']]},
  {id:'motion',number:'01 / OBSERVE & MEASURE',title:'Movement,<br><em>made visible.</em>',
    description:'A dedicated capture platform brings cameras, calibration targets and movement studies into one focused space.',
    position:[-8.4,2.25,5.2],target:[-8.55,1.55,-1.4],image:'motion',
    details:[['Capture rig','Editable uprights, lens housings, locking collars and data cables define the capture volume.'],['Calibration floor','High contrast floor crosses establish a visible reference grid. This is a design study, not a calibrated measurement system.'],['Motion display','The screen shows illustrative motion graphics. It does not display live capture or measured results.']]},
  {id:'clinical',number:'02 / STUDY & UNDERSTAND',title:'A place for<br><em>closer study.</em>',
    description:'Warm cabinetry, anatomy studies and a quiet analysis desk support observation and thoughtful investigation.',
    position:[-4.5,2,1.4],target:[-4.4,1.7,-4],image:'clinical',
    details:[['Study model','The native editable skeletal sculpture includes ribs, vertebral processes and articulated hand details. It is illustrative, not clinically validated.'],['Anatomy prints','Authored line studies explore form and motion. They are educational design props, not diagnostic references.'],['Analysis desk','A compact work surface integrates storage, task lighting and a dedicated display.']]},
  {id:'engineering',number:'03 / PROTOTYPE & MAKE',title:'From thought<br><em>to tangible.</em>',
    description:'An instrument bench, organized tools and an articulated actuator prototype make experimentation part of daily work.',
    position:[4.4,2.05,1.8],target:[4.95,1.75,-4.2],image:'engineering',
    details:[['Actuator study','A directly authored prototype includes separate links, copper joints, a gripper and wiring loom. It is a visual concept.'],['Electronics bench','Circuit traces, component packages and an instrument mat add a coherent prototyping story.'],['Tool wall','Camera equipment, precision drivers and a caliper sit against a layered walnut and graphite tool wall.']]},
  {id:'projects',number:'04 / CONNECT & PRESENT',title:'Good ideas<br><em>come together.</em>',
    description:'A shared project table creates room for discussion, material studies and the next iteration.',
    position:[9.1,2,3],target:[9.45,1.6,-2.7],image:'projects',
    details:[['Materials table','Walnut, aluminum and copper samples connect the room palette to the design process.'],['Project wall','The pin-up studies and presentation display contain authored concept content, not client work.'],['Shared seating','Woven seat pads, polished supports and restrained lighting support a quieter collaborative zone.']]}
];

export function zoneFromHash(hash: string): Zone {
  return zones.find(z => z.id === hash.replace(/^#/, '')) ?? zones[0];
}

export const anchors:Record<ZoneId,Point[]>={
  home:[[0,1.6,-3.0],[-.6,.45,2.8],[0,3.0,-5.7]],
  motion:[[-10.4,2.35,.4],[-8.55,.25,-1.0],[-7.3,1.5,-2.2]],
  clinical:[[-5.39,1.3,-3.13],[-4.7,2.4,-4.79],[-4.3,.85,-3.78]],
  engineering:[[5.6,1.3,-4],[5,.88,-3.86],[4.9,2.1,-4.7]],
  projects:[[9.4,.88,-1.8],[10.55,2.5,-4.85],[8.6,.7,-.8]]
};

export function blend(a: Point, b: Point, t: number): Point {
  const v = Math.min(1, Math.max(0,t));
  const e = v*v*(3-2*v);
  return a.map((n,i) => n+(b[i]-n)*e) as Point;
}
