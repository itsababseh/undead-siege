import re

with open('index.html', 'r') as f:
    code = f.read()

# ============================================================
# FIX 1: Redesign the map — make East Chamber a proper big room
# The current east chamber is only cols 21-22, rows 11-18 (tiny!)
# New design: east chamber is cols 20-22, rows 10-18 with proper interior
# Also fix west wing connectivity
# ============================================================
old_map = """var map=[
//0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3
  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, //0
  1,3,3,3,3,3,3,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //1
  1,3,0,0,0,0,0,0,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //2
  1,3,0,0,0,0,0,0,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //3
  1,3,0,0,0,0,0,0,3,1,0,0,2,2,0,0,0,0,2,2,0,0,0,1, //4
  1,3,0,0,0,0,0,0,3,1,0,0,2,0,0,0,0,0,0,2,0,0,0,1, //5
  1,3,0,0,0,0,0,0,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //6
  1,3,0,0,0,0,0,0,3,4,0,0,0,0,0,3,3,0,0,0,0,0,0,1, //7
  1,3,0,0,0,0,0,0,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //8
  1,3,3,3,3,3,3,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //9
  1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1, //10
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,1, //11
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,1, //12
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,1, //13
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1, //14
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1, //15
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1, //16
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,0,0,1,0,0,1, //17
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,1, //18
  1,0,0,2,2,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,1,1,1,1, //19
  1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,1, //20
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //21
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //22
  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, //23
];"""

new_map = """var map=[
//0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3
  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, //0
  1,3,3,3,3,3,3,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //1
  1,3,0,0,0,0,0,0,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //2
  1,3,0,0,0,0,0,0,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //3
  1,3,0,0,0,0,0,0,3,1,0,0,2,2,0,0,0,0,2,2,0,0,0,1, //4
  1,3,0,0,0,0,0,0,3,1,0,0,2,0,0,0,0,0,0,2,0,0,0,1, //5
  1,3,0,0,0,0,0,0,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //6
  1,3,0,0,0,0,0,0,3,4,0,0,0,0,0,3,3,0,0,0,0,0,0,1, //7
  1,3,0,0,0,0,0,0,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //8
  1,3,3,3,3,3,3,3,3,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1, //9
  1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,2,2,2,1, //10
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,1, //11
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,1, //12
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1, //13
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1, //14
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1, //15
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,0,1,0,0,0,1, //16
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1, //17
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,1, //18
  1,0,0,2,2,0,0,0,0,0,0,2,2,0,0,0,0,0,0,1,1,1,1,1, //19
  1,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,1, //20
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //21
  1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1, //22
  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, //23
];"""

code = code.replace(old_map, new_map)

# ============================================================
# FIX 2: Update door tiles to match new map (east door now at col 19)
# ============================================================
old_doors = """var doors=[
  {id:'west',tiles:[[9,7],[9,8]],cost:1250,opened:false,label:'West Wing'},
  {id:'east',tiles:[[20,12],[20,13]],cost:2000,opened:false,label:'East Chamber'},
];"""

new_doors = """var doors=[
  {id:'west',tiles:[[9,7],[9,8]],cost:1250,opened:false,label:'West Wing'},
  {id:'east',tiles:[[19,11],[19,12]],cost:2000,opened:false,label:'East Chamber'},
];"""

code = code.replace(old_doors, new_doors)

# Fix door reset in initGame to match new tile positions
old_door_reset = """    for(var di=0;di<doors.length;di++){
    doors[di].opened=false;
    for(var dt=0;dt<doors[di].tiles.length;dt++){
      var dx=doors[di].tiles[dt][0],dy=doors[di].tiles[dt][1];
      map[dy*MAP_W+dx]=(doors[di].id==='west'?4:5);
    }
  }"""

new_door_reset = """    for(var di=0;di<doors.length;di++){
    doors[di].opened=false;
    for(var dt=0;dt<doors[di].tiles.length;dt++){
      var dx=doors[di].tiles[dt][0],dy=doors[di].tiles[dt][1];
      map[dy*MAP_W+dx]=(doors[di].id==='west'?4:5);
    }
  }
  doorsOpenedCount=0;"""

code = code.replace(old_door_reset, new_door_reset)

# ============================================================
# FIX 3: Update east chamber spawn points to match new room layout
# ============================================================
old_spawns = """  // East chamber spawns (only when east door opened)
  {x:22*TILE,y:12*TILE,door:'east'},{x:22*TILE,y:16*TILE,door:'east'},
  {x:21.5*TILE,y:14*TILE,door:'east'},{x:22*TILE,y:18*TILE,door:'east'},"""

new_spawns = """  // East chamber spawns (only when east door opened)
  {x:21*TILE,y:11*TILE,door:'east'},{x:22*TILE,y:13*TILE,door:'east'},
  {x:21*TILE,y:15*TILE,door:'east'},{x:22*TILE,y:17*TILE,door:'east'},
  {x:20.5*TILE,y:14*TILE,door:'east'},{x:22*TILE,y:18*TILE,door:'east'},"""

code = code.replace(old_spawns, new_spawns)

# ============================================================
# FIX 4: Update Quick Revive perk machine to be inside the new east chamber
# ============================================================
code = code.replace(
    "{tx:22,ty:15,perkIdx:3}, // Quick Revive - east chamber (need door)",
    "{tx:21,ty:14,perkIdx:3}, // Quick Revive - east chamber (need door)"
)

# ============================================================
# FIX 5: Zombie stuck detection + simple wall-sliding pathfinding
# Replace the zombie movement section in update()
# ============================================================
old_zombie_move = """    if(d>20){
      var mx=dx/d*z.spd*dt,my=dy/d*z.spd*dt;
      for(var j=0;j<zombies.length;j++){
        var oz=zombies[j];
        if(oz===z)continue;
        var sx=z.x-oz.x,sy=z.y-oz.y;
        var sd=Math.hypot(sx,sy);
        if(sd<30&&sd>0.1){
          mx+=sx/sd*0.5*dt*60;
          my+=sy/sd*0.5*dt*60;
        }
      }
      var nx=z.x+mx,ny=z.y+my;
      if(mapAt(nx,z.y)===0)z.x=nx;
      if(mapAt(z.x,ny)===0)z.y=ny;
    }"""

new_zombie_move = """    if(d>20){
      var mx=dx/d*z.spd*dt,my=dy/d*z.spd*dt;
      // Separation from other zombies
      for(var j=0;j<zombies.length;j++){
        var oz=zombies[j];
        if(oz===z)continue;
        var sx=z.x-oz.x,sy=z.y-oz.y;
        var sd=Math.hypot(sx,sy);
        if(sd<30&&sd>0.1){
          mx+=sx/sd*0.5*dt*60;
          my+=sy/sd*0.5*dt*60;
        }
      }
      var nx=z.x+mx,ny=z.y+my;
      var movedX=false,movedY=false;
      // Try both axes independently for wall sliding
      if(mapAt(nx,z.y)===0){z.x=nx;movedX=true;}
      if(mapAt(z.x,ny)===0){z.y=ny;movedY=true;}
      // If blocked on both axes, try wall-hugging
      if(!movedX&&!movedY){
        // Try perpendicular directions to slide along walls
        var perpX=(-dy/d)*z.spd*dt*0.7;
        var perpY=(dx/d)*z.spd*dt*0.7;
        if(mapAt(z.x+perpX,z.y)===0){z.x+=perpX;movedX=true;}
        else if(mapAt(z.x-perpX,z.y)===0){z.x-=perpX;movedX=true;}
        if(mapAt(z.x,z.y+perpY)===0){z.y+=perpY;movedY=true;}
        else if(mapAt(z.x,z.y-perpY)===0){z.y-=perpY;movedY=true;}
      }
      // Stuck detection: track position over time
      if(!z.stuckCheck){z.stuckCheck={x:z.x,y:z.y,timer:0};}
      z.stuckCheck.timer+=dt;
      if(z.stuckCheck.timer>=3){
        var stuckDist=Math.hypot(z.x-z.stuckCheck.x,z.y-z.stuckCheck.y);
        if(stuckDist<TILE*0.5){
          // Zombie is stuck — teleport to nearest valid spawn
          var bestSp=null,bestSpD=Infinity;
          for(var si=0;si<spawnPts.length;si++){
            var sp=spawnPts[si];
            if(sp.door){
              var dOpen=false;
              for(var ddi=0;ddi<doors.length;ddi++){if(doors[ddi].id===sp.door&&doors[ddi].opened)dOpen=true;}
              if(!dOpen)continue;
            }
            if(mapAt(sp.x,sp.y)!==0)continue;
            var spD=Math.hypot(sp.x-player.x,sp.y-player.y);
            // Pick spawn closest to player (so they approach from a new angle)
            if(spD>TILE*3&&spD<bestSpD){bestSpD=spD;bestSp=sp;}
          }
          if(bestSp){z.x=bestSp.x+(Math.random()-0.5)*30;z.y=bestSp.y+(Math.random()-0.5)*30;}
        }
        z.stuckCheck={x:z.x,y:z.y,timer:0};
      }
    }"""

code = code.replace(old_zombie_move, new_zombie_move)

# ============================================================
# FIX 6: Increase zombie count when doors are opened
# Add doorsOpenedCount variable and modify tryBuyDoor
# ============================================================

# Add doorsOpenedCount variable after the state variables
code = code.replace(
    "let dmgFlash=0,gunKick=0,gunBob=0;",
    "let dmgFlash=0,gunKick=0,gunBob=0;\nvar doorsOpenedCount=0;"
)

# Update tryBuyDoor to increase zombie counts
old_buy_door = """        if(points>=door.cost){
          points-=door.cost;
          door.opened=true;
          // Remove door tiles from map (set to 0)
          for(var dt=0;dt<door.tiles.length;dt++){
            var dx=door.tiles[dt][0],dy=door.tiles[dt][1];
            map[dy*MAP_W+dx]=0;
          }
          beep(300,'sine',0.15,0.15);
          setTimeout(function(){beep(200,'sine',0.2,0.1);},100);
          texts.push({text:door.label+' OPENED!',x:screenW/2,y:screenH/2-40,life:2.5,color:'#4f4'});"""

new_buy_door = """        if(points>=door.cost){
          points-=door.cost;
          door.opened=true;
          doorsOpenedCount++;
          // Remove door tiles from map (set to 0)
          for(var dt=0;dt<door.tiles.length;dt++){
            var dx=door.tiles[dt][0],dy=door.tiles[dt][1];
            map[dy*MAP_W+dx]=0;
          }
          beep(300,'sine',0.15,0.15);
          setTimeout(function(){beep(200,'sine',0.2,0.1);},100);
          // Increase zombie count: +4 to spawn for this round, +2 max alive
          zToSpawn+=4;
          maxAlive=Math.min(maxAlive+3,30);
          texts.push({text:door.label+' OPENED!',x:screenW/2,y:screenH/2-40,life:2.5,color:'#4f4'});
          texts.push({text:'More zombies incoming!',x:screenW/2,y:screenH/2-15,life:2,color:'#f84'});"""

code = code.replace(old_buy_door, new_buy_door)

# Also increase base zombie counts per round based on doors opened
old_next_round = """  zToSpawn=Math.floor(6+round*3);
  zSpawned=0;
  maxAlive=Math.min(6+round*2,24);"""

new_next_round = """  zToSpawn=Math.floor(6+round*3+doorsOpenedCount*2);
  zSpawned=0;
  maxAlive=Math.min(6+round*2+doorsOpenedCount*2,30);"""

code = code.replace(old_next_round, new_next_round)

# ============================================================
# FIX 7: Add pause system (Escape key)
# ============================================================

# Add pause state variable
code = code.replace(
    "let state='menu';",
    "let state='menu';\nlet paused=false;"
)

# Add Escape key handler + add escape to gameKeys
code = code.replace(
    "var gameKeys=['w','a','s','d','r','e','1','2','3',' '];",
    "var gameKeys=['w','a','s','d','r','e','1','2','3',' ','escape'];"
)

# Add Escape handling in the keydown listener
old_keydown = """document.addEventListener('keydown',function(e){
  var k=e.key.toLowerCase();
  keys[k]=true;
  if(gameKeys.indexOf(k)>=0)e.preventDefault();
});"""

new_keydown = """document.addEventListener('keydown',function(e){
  var k=e.key.toLowerCase();
  keys[k]=true;
  if(gameKeys.indexOf(k)>=0)e.preventDefault();
  // Pause toggle on Escape
  if(k==='escape'&&(state==='playing'||state==='roundIntro')){
    paused=!paused;
    if(paused){document.exitPointerLock();}
    else{canvas.requestPointerLock();}
  }
});"""

code = code.replace(old_keydown, new_keydown)

# Add pause check at the start of update()
old_update_start = """function update(dt){
  if(state==='roundIntro'){"""

new_update_start = """function update(dt){
  if(paused)return;
  if(state==='roundIntro'){"""

code = code.replace(old_update_start, new_update_start)

# Add pause overlay in game loop rendering
old_loop_render = """  if(state!=='menu'){
    update(dt);
    ctx.fillStyle='#000';
    ctx.fillRect(0,0,screenW,screenH);
    castRays();
    renderPerkMachines();
    renderZombies();
    drawHUD();
    drawMinimap();
  }"""

new_loop_render = """  if(state!=='menu'){
    update(dt);
    ctx.fillStyle='#000';
    ctx.fillRect(0,0,screenW,screenH);
    castRays();
    renderPerkMachines();
    renderZombies();
    drawHUD();
    drawMinimap();
    // Pause overlay
    if(paused){
      ctx.fillStyle='rgba(0,0,0,0.7)';
      ctx.fillRect(0,0,screenW,screenH);
      ctx.fillStyle='#fff';
      ctx.font='bold 48px Courier New';
      ctx.textAlign='center';
      ctx.fillText('PAUSED',screenW/2,screenH/2-30);
      ctx.fillStyle='#888';
      ctx.font='16px Courier New';
      ctx.fillText('Press ESC to resume',screenW/2,screenH/2+15);
      ctx.font='12px Courier New';
      ctx.fillText('Round '+round+' · '+totalKills+' kills · $'+points,screenW/2,screenH/2+45);
      // Show owned perks
      var pLines=[];
      for(var pi=0;pi<perks.length;pi++){
        if(player.perksOwned[perks[pi].id])pLines.push(perks[pi].name+' ('+perks[pi].desc+')');
      }
      if(pLines.length>0){
        ctx.fillStyle='#aaa';
        ctx.font='12px Courier New';
        ctx.fillText('PERKS: '+pLines.join(' · '),screenW/2,screenH/2+70);
      }
      ctx.fillStyle='#555';
      ctx.font='11px Courier New';
      ctx.fillText('Perks are permanent until death (like CoD Zombies)',screenW/2,screenH/2+95);
    }
  }"""

code = code.replace(old_loop_render, new_loop_render)

# Reset pause on game start and death
code = code.replace(
    "function startGame(){\n  overlay.classList.add('hidden');",
    "function startGame(){\n  paused=false;\n  overlay.classList.add('hidden');"
)

# ============================================================
# FIX 8: Better perk feedback when purchased
# ============================================================
old_perk_buy = """        points-=perk.cost;
        player.perksOwned[perk.id]=true;
        perk.apply();
        // Perk jingle
        beep(400,'sine',0.1,0.1);setTimeout(function(){beep(500,'sine',0.1,0.1);},80);
        setTimeout(function(){beep(600,'sine',0.1,0.1);},160);setTimeout(function(){beep(800,'sine',0.15,0.12);},240);
        texts.push({text:perk.name+'!',x:screenW/2,y:screenH/2-40,life:2,color:perk.color});"""

new_perk_buy = """        points-=perk.cost;
        player.perksOwned[perk.id]=true;
        perk.apply();
        // Perk jingle
        beep(400,'sine',0.1,0.1);setTimeout(function(){beep(500,'sine',0.1,0.1);},80);
        setTimeout(function(){beep(600,'sine',0.1,0.1);},160);setTimeout(function(){beep(800,'sine',0.15,0.12);},240);
        texts.push({text:perk.name+' ACTIVE!',x:screenW/2,y:screenH/2-50,life:2.5,color:perk.color});
        texts.push({text:perk.desc+' · Permanent until death',x:screenW/2,y:screenH/2-25,life:2.5,color:'#aaa'});"""

code = code.replace(old_perk_buy, new_perk_buy)

# ============================================================
# FIX 9: Update controls text to include Escape
# ============================================================
code = code.replace(
    "WASD move · Mouse aim · Click shoot<br>\nR reload · 1-3 switch weapons · E buy",
    "WASD move · Mouse aim · Click shoot<br>\nR reload · 1-3 switch weapons · E buy · ESC pause"
)

with open('index.html', 'w') as f:
    f.write(code)

print("All patches applied successfully!")
print(f"File size: {len(code)} characters")
