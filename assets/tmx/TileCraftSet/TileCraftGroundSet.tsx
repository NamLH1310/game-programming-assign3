<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.9" tiledversion="1.9.2" name="TileCraftGroundSet" tilewidth="16" tileheight="16" tilecount="81" columns="9">
 <image source="TileCraftGroundSet.png" width="144" height="144"/>
 <tile id="3">
  <objectgroup draworder="index" id="3">
   <object id="2" name="land_border" class="border" x="3.2288" y="2.05072" width="12.7843" height="13.9187"/>
  </objectgroup>
 </tile>
 <tile id="4">
  <objectgroup draworder="index" id="3">
   <object id="3" name="land_border" class="border" x="0.17453" y="1.00355" width="15.7949" height="14.9659"/>
  </objectgroup>
 </tile>
 <tile id="5">
  <objectgroup draworder="index" id="3">
   <object id="2" name="land_border" class="border" x="0.0436324" y="1.09081" width="13.7878" height="14.9659"/>
  </objectgroup>
 </tile>
 <tile id="12">
  <objectgroup draworder="index" id="2">
   <object id="1" name="land_border" class="border" x="2.92337" y="0.261794" width="13.0025" height="15.6204"/>
  </objectgroup>
 </tile>
 <tile id="14">
  <objectgroup draworder="index" id="2">
   <object id="1" name="land_border" class="border" x="0.0872648" y="0.130897" width="15.0532" height="15.9258"/>
  </objectgroup>
 </tile>
 <tile id="21">
  <objectgroup draworder="index" id="2">
   <object id="1" name="land_border" class="border" x="3.01064" y="0.130897" width="13.0461" height="15.2713"/>
  </objectgroup>
 </tile>
 <tile id="22">
  <objectgroup draworder="index" id="2">
   <object id="1" name="land_border" class="border" x="0.0872648" y="0.130897" width="15.8822" height="15.1841"/>
  </objectgroup>
 </tile>
 <tile id="23">
  <objectgroup draworder="index" id="2">
   <object id="1" name="land_border" class="border" x="0.0436324" y="0.0872648" width="14.4423" height="15.2277"/>
  </objectgroup>
 </tile>
 <tile id="30">
  <objectgroup draworder="index" id="2">
   <object id="1" name="land_border" class="border" x="0.181818" y="0.272727">
    <polygon points="0,0 15.6364,-0.0909091 15.5455,9.72727 10.3636,15.3636 0.0909091,15.5455"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="31">
  <objectgroup draworder="index" id="2">
   <object id="1" name="land_border" class="border" x="0.0909091" y="10.5455">
    <polygon points="0,0 5.45455,5.27273 15.9091,5.36364 15.8182,-10.5455 0,-10.5455"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="39">
  <objectgroup draworder="index" id="2">
   <object id="1" name="land_border" class="border" x="9.1628" y="0.17453">
    <polygon points="1.00355,-0.17453 6.80665,6.45759 6.76302,15.7949 -9.1628,15.7513 -9.20644,-0.17453"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="40">
  <objectgroup draworder="index" id="2">
   <object id="1" name="land_border" class="border" x="5.62858" y="0.17453">
    <polygon points="0.261794,-0.0872648 -5.58495,4.66867 -5.58495,15.5768 10.2972,15.664 10.2972,-0.17453"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="71" probability="0.2"/>
 <wangsets>
  <wangset name="corner" type="corner" tile="-1">
   <wangcolor name="grass" color="#00ff00" tile="-1" probability="1"/>
   <wangcolor name="water" color="#0000ff" tile="-1" probability="1"/>
   <wangtile tileid="3" wangid="0,1,0,2,0,1,0,1"/>
   <wangtile tileid="4" wangid="0,1,0,2,0,2,0,1"/>
   <wangtile tileid="5" wangid="0,1,0,1,0,2,0,1"/>
   <wangtile tileid="12" wangid="0,2,0,2,0,1,0,1"/>
   <wangtile tileid="13" wangid="0,2,0,2,0,2,0,2"/>
   <wangtile tileid="14" wangid="0,1,0,1,0,2,0,2"/>
   <wangtile tileid="21" wangid="0,2,0,1,0,1,0,1"/>
   <wangtile tileid="22" wangid="0,2,0,1,0,1,0,2"/>
   <wangtile tileid="23" wangid="0,1,0,1,0,1,0,2"/>
   <wangtile tileid="30" wangid="0,2,0,1,0,2,0,2"/>
   <wangtile tileid="31" wangid="0,2,0,2,0,1,0,2"/>
   <wangtile tileid="39" wangid="0,1,0,2,0,2,0,2"/>
   <wangtile tileid="40" wangid="0,2,0,2,0,2,0,1"/>
   <wangtile tileid="41" wangid="0,1,0,1,0,1,0,1"/>
  </wangset>
 </wangsets>
</tileset>
