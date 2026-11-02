#!/usr/bin/env python3
"""Adds Cartbench's activity recorder to Stellerator's prebuilt worker.
Usage: patch-worker.py original-stellerator.js output.js"""
import sys
REC = r'''/* Cartbench activity recorder */
self.__cb=(()=>{let size=0,first=-1,count=0,bank=0,start=0,rom=null,cov=null,pc=-9,ld=-1,ldv=0,lo=-1,lov=0,bad=0,tot=0,dirty=!1;
const off=a=>size<=2048?a&2047:size<=4096?a&4095:bank*4096+(a&4095);
const hot=a=>{const h=(a&4095)-first;if(first>=0&&h>=0&&h<count)bank=h};
const c={f:0,r(a,v){if(!cov)return;hot(a);const o=off(a);if(o>=size)return;tot++;if(rom[o]!==v)bad++;
if(c.f){if(!(cov[o]&1)){cov[o]|=1;dirty=!0}pc=o}
else if(o>pc&&o<=pc+3){if(o<=pc+2){lo=o;lov=v}}
else{if(!(cov[o]&2)){cov[o]|=2;dirty=!0}ld=o;ldv=v}},
w(a,v){if(!cov)return;if(a&4096){hot(a);return}if(a&128)return;const r=a&63;
const fl=r===27||r===28?4:r>=13&&r<=15?8:r>=6&&r<=9?16:0;if(!fl)return;
if(ld>=0&&ldv===v){if(!(cov[ld]&fl)){cov[ld]|=fl;dirty=!0}}
else if(fl===16&&lo>=0&&lov===v&&!(cov[lo]&32)){cov[lo]|=48;dirty=!0}}};
self.addEventListener("message",e=>{const m=e.data&&e.data.cbConfig;if(!m)return;e.stopImmediatePropagation();
size=m.rom.length;rom=m.rom;first=m.first;count=m.count;bank=m.start;cov=new Uint8Array(size);pc=-9;ld=-1;lo=-1;bad=0;tot=0;dirty=!1});
setInterval(()=>{if(dirty&&cov){dirty=!1;self.postMessage({cbCov:cov.slice(),bad,tot})}},400);return c})();
'''
PATCHES = [
 ('this._lastDataBusValue=this._cartridge.read(t),this.event.read.dispatch(2)',
  'this._lastDataBusValue=this._cartridge.read(t),__cb.r(t,this._lastDataBusValue),this.event.read.dispatch(2)'),
 ('write(t,e){this._lastDataBusValue=e,t&=8191,this.event.transition.dispatch(t),this._lastAddressBusValue=t,',
  'write(t,e){this._lastDataBusValue=e,t&=8191,this.event.transition.dispatch(t),this._lastAddressBusValue=t,__cb.w(t,e),'),
 ('const e=this._bus.read(this.state.p);this.state.nmi?',
  '__cb.f=1;const e=this._bus.read(this.state.p);__cb.f=0;this.state.nmi?'),
 ('_fetch(){const t=P.opcodes[this._bus.read(this.state.p)];let e,',
  '_fetch(){__cb.f=1;const t=P.opcodes[this._bus.read(this.state.p)];__cb.f=0;let e,'),
]
s = open(sys.argv[1], encoding='utf8').read()
for a, b in PATCHES:
    if s.count(a) != 1: sys.exit('anchor not found exactly once: ' + a)
    s = s.replace(a, b)
s = s.replace('//# sourceMappingURL=stellerator.js.map', '')
open(sys.argv[2], 'w', encoding='utf8').write(REC + s)
