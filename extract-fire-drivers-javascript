// The javascript code can be accessed through Google Earth Engine cloud computing platform at:
// https://code.earthengine.google.com/93b518d230de2e8aaa2b84e909d56e9e


// The code is as follows:
var LAICol = ee.ImageCollection("MODIS/006/MOD15A2H"),
    treeCover = ee.ImageCollection("MODIS/006/MOD44B"),
    MODIS_ET = ee.ImageCollection("MODIS/006/MOD16A2"),
    MODIS_albedo = ee.ImageCollection("MODIS/006/MCD43A3"),
    MODIS_LandCover = ee.ImageCollection("MODIS/006/MCD12Q1"),
    ecoRegions = ee.FeatureCollection("RESOLVE/ECOREGIONS/2017"),
    MODIS_precip = ee.ImageCollection("NASA/GPM_L3/IMERG_V06"),
    MODIS_veg = ee.ImageCollection("MODIS/006/MOD13A2"),
    landData = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H"),
    Basin = ee.FeatureCollection("WWF/HydroSHEDS/v1/Basins/hybas_2"),
    ERA5 = ee.ImageCollection("ECMWF/ERA5_LAND/HOURLY"),
    IncomingLR = ee.Image("users/yunxiaz1/radiation/incomLR_CERES_SYN1deg-Month_Terra-Aqua-MODIS_200110-202009"),
    IncomingSR = ee.Image("users/yunxiaz1/radiation/incomSR_CERES_SYN1deg-Month_Terra-Aqua-MODIS_200110-202009"),
    table1 = ee.FeatureCollection("users/yunxiaz1/burnSnow_burns_unbns_100km/BurnImage8_20021001to20031001WithLonLat_burnOnce-0000013568-0000027136_burn_7469"),
    table2 = ee.FeatureCollection("users/yunxiaz1/burnSnow_burns_unbns_100km/BurnImage8_20021001to20031001WithLonLat_burnOnce-0000013568-0000027136_unbn_7469"),
    table3 = ee.FeatureCollection("users/yunxiaz1/burnSnow_burns_unbns_100km/BurnImage8_20031001to20041001WithLonLat_burnOnce-0000013568-0000027136_burn_6913"),
    table4 = ee.FeatureCollection("users/yunxiaz1/burnSnow_burns_unbns_100km/BurnImage8_20031001to20041001WithLonLat_burnOnce-0000013568-0000027136_unbn_6913"),
    table5 = ee.FeatureCollection("users/yunxiaz1/burnSnow_burns_unbns_100km/BurnImage8_20041001to20051001WithLonLat_burnOnce-0000013568-0000027136_burn_7179"),
    table6 = ee.FeatureCollection("users/yunxiaz1/burnSnow_burns_unbns_100km/BurnImage8_20041001to20051001WithLonLat_burnOnce-0000013568-0000027136_unbn_7179"),
    MODIS_LST = ee.ImageCollection("MODIS/006/MOD11A1"),
    snowCover = ee.ImageCollection("MODIS/006/MOD10A1");


  




var roi = /* color: #bf04c2 */ee.Geometry.Polygon(
        [[[-180, 82],
          [0, 82],
          [180, 82],
          [180, 0],
          [0, 0],
          [-180, 0]]], null, false);
var Vis = {
  min: 13000.0,
  max: 16500.0,
  palette: [
    '040274', '040281', '0502a3', '0502b8', '0502ce', '0502e6',
    '0602ff', '235cb1', '307ef3', '269db1', '30c8e2', '32d3ef',
    '3be285', '3ff38f', '86e26f', '3ae237', 'b5e22e', 'd6e21f',
    'fff705', 'ffd611', 'ffb613', 'ff8b13', 'ff6e08', 'ff500d',
    'ff0000', 'de0101', 'c21301', 'a71001', '911003'
  ],
};

// ************************************************************ Extract Fire Drivers ******************************************************************************************

function getAccu_precip_snow(year, month, start, finish){
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  
  var bandName = 'precipitationCal';
  var Scale = 0.5;
  var unit = 'mm/month'
  var imgCol_precip = getDailyData_sum(MODIS_precip, startDate, endDate, bandName)
  // var imgCol_precip = getMosaicImageCol(imgCol_precip, start, finish);
  imgCol_precip = imgCol_precip.map(function(image){
                                var time_start = image.get("system:time_start");
                                image = image.multiply(Scale).toDouble();
                                image = image.set("system:time_start", time_start);
                                return image;
                              })

  
  var bandName = 'temperature_2m';
  var unit = 'degree';
  var imgCol = getDailyData_mean(ERA5, start, finish, bandName);
  var imgCol_temp = imgCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.subtract(273.15).toDouble();
    image = image.rename(bandName)
    image = image.set("system:time_start", time_start);
    return image;
  });
  

  var imgCol_precip_temp = imgCol_precip.combine(imgCol_temp);

  var imgCol_precip_snow = imgCol_precip_temp.map(function(image) {
                                             var time_start = image.get("system:time_start");
                                             var image_precip = image.select('precipitationCal')
                                             var image_temp = image.select('temperature_2m')
                                             
                                             var mask = image_temp.lt(2);
                                             var image_precip = image_precip.multiply(mask);
                                            
                                            var image_precip = image_precip.select('precipitationCal');
                                             return image_precip.set("system:time_start", time_start);
                                           });
  var imgCol_precip_snow = imgCol_precip_snow.sum()
  var img_precip_snow = imgCol_precip_snow.rename('Accu_precip_snow')
  return img_precip_snow
}

function getAccu_precip_snow_LST(year, month, start, finish){
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  
  var bandName = 'precipitationCal';
  var Scale = 0.5;
  var unit = 'mm/month'
  var imgCol_precip = getDailyData_sum(MODIS_precip, startDate, endDate, bandName)
  // var imgCol_precip = getMosaicImageCol(imgCol_precip, start, finish);
  imgCol_precip = imgCol_precip.map(function(image){
                                var time_start = image.get("system:time_start");
                                image = image.multiply(Scale).toDouble();
                                image = image.set("system:time_start", time_start);
                                return image;
                              })

  
  // var bandName = 'temperature_2m';
  // var unit = 'degree';
  // var imgCol = getDailyData_mean(ERA5, start, finish, bandName);
  // var imgCol_temp = imgCol.map(function(image){
  //                           var time_start = image.get("system:time_start");
  //                           image = image.subtract(273.15).toDouble();
  //                           image = image.rename(bandName)
  //                           image = image.set("system:time_start", time_start);
  //                           return image;
  //                         });
  
  var bandName = "LST_Day_1km"
  var bandName2 = "LST_MODIS"
  var Scale = 0.02;
  var unit = 'Land Surface Temperature: K'
  var imgCol_LST = MODIS_LST.filterDate(startDate, endDate);
  // var imgCol_LST = getMosaicImageCol(imgCol_LST, start, finish);
  var imgCol_LST = imgCol_LST.select(["LST_Day_1km","LST_Night_1km"]);
  imgCol_LST = imgCol_LST.map(function(image){
                          var time_start = image.get("system:time_start");
                          var image_1 = image.select("LST_Day_1km");
                          var image_2 = image.select("LST_Night_1km");
                          var image_mean = image_1.add(image_2).divide(2);
                          image_mean = image_mean.multiply(Scale).toDouble();
                          image_mean = image_mean.subtract(273.15).toDouble();
                          image_mean = image_mean.rename(bandName2);
                          image_mean = image_mean.set("system:time_start", time_start);
                          return image_mean;
                        })

  
  var imgCol_temp = imgCol_LST
  
  var imgCol_precip_temp = imgCol_precip.combine(imgCol_temp);

  var imgCol_precip_snow = imgCol_precip_temp.map(function(image) {
                                             var time_start = image.get("system:time_start");
                                             var image_precip = image.select('precipitationCal')
                                             var image_temp = image.select('LST_MODIS')
                                             
                                             var mask = image_temp.lt(0);
                                             var image_precip = image_precip.multiply(mask);
                                            
                                            var image_precip = image_precip.select('precipitationCal');
                                             return image_precip.set("system:time_start", time_start);
                                           });
  var imgCol_precip_snow = imgCol_precip_snow.sum()
  var img_precip_snow = imgCol_precip_snow.rename('Accu_precip_snow_LST')
  return img_precip_snow
}



function getSnowmelt_temp(year, month, start, finish){
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);

  var bandName = 'temperature_2m';
  var unit = 'degree';
  var imgCol_temp = getDailyData_mean(ERA5, startDate, endDate,bandName);
  imgCol_temp = imgCol_temp.map(function(image){
                            var time_start = image.get("system:time_start");
                            image = image.subtract(273.15).toDouble();
                            image = image.set("system:time_start", time_start);
                            return image;
                          });

  var imgCol_snowmelt_temp = imgCol_temp.map(function(image){
                              var time_start = image.get("system:time_start");
                              var mask_1 = image.select(["temperature_2m"]).gte(1);
                              var mask_2 = image.select(["temperature_2m"]).lt(1);
                              var mask_3 = image.gte(1).or(image.lt(-2))
                              var value_1 = 0.08
                              var value_2 = 0.04
                              var value_3 = 0.0667
                              var value = 0.0133
                              
                              var image_2 = image.multiply(value)
                              image_2 = image_2.add(value_3)
                              var image_snow_density = mask_1.multiply(value_1).add(mask_2.multiply(value_2)).add(image_2.multiply(mask_3.not()));
                              image_snowmelt_temp = image_snow_density.multiply(1.1).multiply(10).multiply(image);
                              var mask = image_snowmelt_temp.gt(0);
                              var image_snowmelt_temp = image_snowmelt_temp.updateMask(mask);
                              var image_snowmelt_temp = image_snowmelt_temp.set("system:time_start", time_start);
                              return image_snowmelt_temp
                            });
                           

  var img_snowmelt_temp = imgCol_snowmelt_temp.sum() // unit: cm/month
  
  // print(img_snowmelt_temp)
  return img_snowmelt_temp.rename('snowmelt_temp')
  
}


function getSnowmelt_temp_LST(year, month, start, finish){
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);

  // var bandName = 'temperature_2m';
  // var unit = 'degree';
  // var imgCol_temp = getDailyData_mean(ERA5, startDate, endDate,bandName);
  // imgCol_temp = imgCol_temp.map(function(image){
  //                           var time_start = image.get("system:time_start");
  //                           image = image.subtract(273.15).toDouble();
  //                           image = image.set("system:time_start", time_start);
  //                           return image;
  //                         });

  var bandName = "LST_Day_1km"
  var bandName2 = "LST_MODIS"
  var Scale = 0.02;
  var unit = 'Land Surface Temperature: K'
  var imgCol_LST = MODIS_LST.filterDate(startDate, endDate);
  // var imgCol_LST = getMosaicImageCol(imgCol_LST, start, finish);
  var imgCol_LST = imgCol_LST.select(["LST_Day_1km","LST_Night_1km"]);
  imgCol_LST = imgCol_LST.map(function(image){
                          var time_start = image.get("system:time_start");
                          var image_1 = image.select("LST_Day_1km");
                          var image_2 = image.select("LST_Night_1km");
                          var image_mean = image_1.add(image_2).divide(2);
                          image_mean = image_mean.multiply(Scale).toDouble();
                          image_mean = image_mean.subtract(273.15).toDouble();
                          image_mean = image_mean.rename(bandName2);
                          image_mean = image_mean.set("system:time_start", time_start);
                          return image_mean;
                        })

  
  var imgCol_temp = imgCol_LST
  
  
  var imgCol_snowmelt_temp = imgCol_temp.map(function(image){
                              var time_start = image.get("system:time_start");
                              var mask_1 = image.select(["LST_MODIS"]).gte(1);
                              var mask_2 = image.select(["LST_MODIS"]).lt(1);
                              var mask_3 = image.gte(1).or(image.lt(-2))
                              var value_1 = 0.08
                              var value_2 = 0.04
                              var value_3 = 0.0667
                              var value = 0.0133
                              
                              var image_2 = image.multiply(value)
                              image_2 = image_2.add(value_3)
                              var image_snow_density = mask_1.multiply(value_1).add(mask_2.multiply(value_2)).add(image_2.multiply(mask_3.not()));
                              image_snowmelt_temp = image_snow_density.multiply(1.1).multiply(10).multiply(image);
                              var mask = image_snowmelt_temp.gt(0);
                              var image_snowmelt_temp = image_snowmelt_temp.updateMask(mask);
                              var image_snowmelt_temp = image_snowmelt_temp.set("system:time_start", time_start);
                              return image_snowmelt_temp
                            });
                           

  var img_snowmelt_temp = imgCol_snowmelt_temp.sum() // unit: cm/month
  
  // print(img_snowmelt_temp)
  return img_snowmelt_temp.rename('snowmelt_temp_LST')
  
}


function getSnowmelt_rad(year, month, start, finish) {
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  


  var bandName = "Lai_500m"
  var bandName2 = "skyView"
  var Scale = 0.1;
  var unit = 'Leaf Area Index: sq. meter/sq. meter (per month)'
  var ImageCol_lai = LAICol.filterDate(startDate, endDate);
  // var ImageCol_lai = getMosaicImageCol(ImageCol_lai, startDate, endDate);
  var ImageCol_lai = ImageCol_lai.select(bandName);
  var imgCol_F = ImageCol_lai.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image_F = image.multiply(-0.5);
    var image_F = image_F.exp();
    image_F = image_F.rename(bandName2)
    image_F = image_F.set("system:time_start", time_start);
    return image_F;
  })
  var image_F = imgCol_F.mean()
  
  var bandName = "LST_Day_1km"
  var bandName2 = "LST_MODIS"
  var Scale = 0.02;
  var unit = 'Land Surface Temperature: K'
  var imgCol_LST = MODIS_LST.filterDate(startDate, endDate);
  // var imgCol_LST = getMosaicImageCol(imgCol_LST, start, finish);
  var imgCol_LST = imgCol_LST.select(["LST_Day_1km","LST_Night_1km"]);
  imgCol_LST = imgCol_LST.map(function(image){
    var time_start = image.get("system:time_start");
    var image_1 = image.select("LST_Day_1km");
    var image_2 = image.select("LST_Night_1km");
    var image_mean = image_1.add(image_2).divide(2);
    image_mean = image_mean.multiply(Scale).toDouble();
    image_mean = image_mean.rename(bandName2);
    image_mean = image_mean.set("system:time_start", time_start);
    return image_mean;
  })
  var imgCol_LST = imgCol_LST.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  });
  
  
  var bandName = 'temperature_2m';
  var unit = 'K';
  var imgCol = getDailyData_mean(ERA5, start, finish, bandName);
  var imgCol_temp = imgCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.toDouble();
    image = image.rename(bandName)
    image = image.set("system:time_start", time_start);
    return image;
  });
    var imgCol_temp = imgCol_temp.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  });

  var bandName = "Albedo_WSA_shortwave"
  var bandName2 = "Albedo_WSA_shortwave_MODIS"
  var Scale = 0.001;
  var unit = 'Albedo percentage: 1, not %'
  var imgCol_albedo = MODIS_albedo.filterDate(startDate, endDate);
  // var imgCol_albedo = getMosaicImageCol(imgCol_albedo, start, finish);
  var imgCol_albedo = imgCol_albedo.select(bandName);
  imgCol_albedo = imgCol_albedo.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.rename(bandName2)
    image = image.set("system:time_start", time_start);
    return image;
  })
  var imgCol_albedo = imgCol_albedo.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  });
  
 
  var bandName = "Emis_31"
  var bandName2 = "Emis_32"
  var Col = MODIS_LST;
  var Scale = 0.002;
  if (month<10) {
  var EMS29 = ee.Image("users/yunxiaz1/MYD11C3_emissiivity_29/"+"EMS"+year+'0'+month);
  }
  if (month>9) {
  var EMS29 = ee.Image("users/yunxiaz1/MYD11C3_emissiivity_29/"+"EMS"+year+month);
  }
  var ImageCol = Col.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(["Emis_31","Emis_32"]);
  imgCol_emissivity = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    var image_1 = image.select("Emis_31");
    var image_2 = image.select("Emis_32");
    var image_sum = image_1.add(image_2);
    image_sum = image_sum.add(EMS29);
    image_sum = image_sum.multiply(Scale).toDouble();
    image_sum = image_sum.toDouble();
    image_sum = image_sum.rename("Emis29_31_32");
    image_sum = image_sum.set("system:time_start", time_start);
    return image_sum;
  })
  var imgCol_emissivity = imgCol_emissivity.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  })
  
  
  var bandName = 12*(year-2001)+month-9
  bandName = 'b' + bandName
  var img_incoming_shorRD = IncomingSR.select(bandName)
  var img_incoming_longRD = IncomingLR.select(bandName);



  var doyList = ee.List(imgCol_albedo.aggregate_array('doy'));
  var imgCol_snowmelt_rad = doyList.map(function(doy){
                                    var img_temp = imgCol_temp.filter(ee.Filter.eq('doy', doy)).first();
                                    var img_LST = imgCol_LST.filter(ee.Filter.eq('doy', doy)).first();
                                    var img_F = image_F;
                                    var img_albedo = imgCol_albedo.filter(ee.Filter.eq('doy', doy)).first();
                                    var img_emissivity = imgCol_emissivity.filter(ee.Filter.eq('doy', doy)).first();
                                    var img_1_minus_F = img_F.multiply(-1);
                                    var img_1_minus_F = img_1_minus_F.add(1);
                                    var img_1_minus_albedo = img_albedo.multiply(-1);
                                    var img_1_minus_albedo = img_1_minus_albedo.add(1);
                                    
                                    var img_snowmelt_shortRD = img_F.multiply(img_1_minus_albedo).multiply(img_incoming_shorRD);
                                    var img_snowmelt_longRD_air = img_F.multiply(img_emissivity).multiply(img_incoming_longRD);
                                    var img_snowmelt_longRD_canopy = img_1_minus_F.multiply(0.98).multiply(1e-8*5.67).multiply(img_temp).multiply(img_temp).multiply(img_temp).multiply(img_temp);
                                    var img_snowmelt_longRD_ref = img_emissivity.multiply(1e-8*5.67).multiply(img_LST).multiply(img_LST).multiply(img_LST).multiply(img_LST);
                                    var img_snowmelt_rad = img_snowmelt_shortRD.add(img_snowmelt_longRD_air).add(img_snowmelt_longRD_canopy).subtract(img_snowmelt_longRD_ref);
                                    img_snowmelt_rad = img_snowmelt_rad.multiply(0.026)
                                    var mask = img_snowmelt_rad.gt(0);
                                    var img_snowmelt_rad = img_snowmelt_rad.updateMask(mask);
                                    var img_snowmelt_rad = img_snowmelt_rad.set('doy', doy);
                                    return img_snowmelt_rad
                                  })
  var imgCol_snowmelt_rad = ee.ImageCollection.fromImages(imgCol_snowmelt_rad);
  var img_snowmelt_rad = imgCol_snowmelt_rad.sum() // unit: cm/month
  img_snowmelt_rad = img_snowmelt_rad.rename('snowmelt_rad')
  return img_snowmelt_rad
  
}


function getSnowmelt_rad_LST(year, month, start, finish) {
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  


  var bandName = "Lai_500m"
  var bandName2 = "skyView"
  var Scale = 0.1;
  var unit = 'Leaf Area Index: sq. meter/sq. meter (per month)'
  var ImageCol_lai = LAICol.filterDate(startDate, endDate);
  // var ImageCol_lai = getMosaicImageCol(ImageCol_lai, startDate, endDate);
  var ImageCol_lai = ImageCol_lai.select(bandName);
  var imgCol_F = ImageCol_lai.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image_F = image.multiply(-0.5);
    var image_F = image_F.exp();
    image_F = image_F.rename(bandName2)
    image_F = image_F.set("system:time_start", time_start);
    return image_F;
  })
  var image_F = imgCol_F.mean()
  
  var bandName = "LST_Day_1km"
  var bandName2 = "LST_MODIS"
  var Scale = 0.02;
  var unit = 'Land Surface Temperature: K'
  var imgCol_LST = MODIS_LST.filterDate(startDate, endDate);
  // var imgCol_LST = getMosaicImageCol(imgCol_LST, start, finish);
  var imgCol_LST = imgCol_LST.select(["LST_Day_1km","LST_Night_1km"]);
  imgCol_LST = imgCol_LST.map(function(image){
    var time_start = image.get("system:time_start");
    var image_1 = image.select("LST_Day_1km");
    var image_2 = image.select("LST_Night_1km");
    var image_mean = image_1.add(image_2).divide(2);
    image_mean = image_mean.multiply(Scale).toDouble();
    image_mean = image_mean.rename(bandName2);
    image_mean = image_mean.set("system:time_start", time_start);
    return image_mean;
  })
  var imgCol_LST = imgCol_LST.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  });
  
  
  // var bandName = 'temperature_2m';
  // var unit = 'K';
  // var imgCol = getDailyData_mean(ERA5, start, finish, bandName);
  // var imgCol_temp = imgCol.map(function(image){
  //   var time_start = image.get("system:time_start");
  //   image = image.toDouble();
  //   image = image.rename(bandName)
  //   image = image.set("system:time_start", time_start);
  //   return image;
  // });
  //   var imgCol_temp = imgCol_temp.map(function(img) {
  // var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  // return img.set('doy', doy);
  // });

  var imgCol_temp  = imgCol_LST
  
  var bandName = "Albedo_WSA_shortwave"
  var bandName2 = "Albedo_WSA_shortwave_MODIS"
  var Scale = 0.001;
  var unit = 'Albedo percentage: 1, not %'
  var imgCol_albedo = MODIS_albedo.filterDate(startDate, endDate);
  // var imgCol_albedo = getMosaicImageCol(imgCol_albedo, start, finish);
  var imgCol_albedo = imgCol_albedo.select(bandName);
  imgCol_albedo = imgCol_albedo.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.rename(bandName2)
    image = image.set("system:time_start", time_start);
    return image;
  })
  var imgCol_albedo = imgCol_albedo.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  });
  
 
  var bandName = "Emis_31"
  var bandName2 = "Emis_32"
  var Col = MODIS_LST;
  var Scale = 0.002;
  if (month<10) {
  var EMS29 = ee.Image("users/yunxiaz1/MYD11C3_emissiivity_29/"+"EMS"+year+'0'+month);
  }
  if (month>9) {
  var EMS29 = ee.Image("users/yunxiaz1/MYD11C3_emissiivity_29/"+"EMS"+year+month);
  }
  var ImageCol = Col.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(["Emis_31","Emis_32"]);
  imgCol_emissivity = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    var image_1 = image.select("Emis_31");
    var image_2 = image.select("Emis_32");
    var image_sum = image_1.add(image_2);
    image_sum = image_sum.add(EMS29);
    image_sum = image_sum.multiply(Scale).toDouble();
    image_sum = image_sum.toDouble();
    image_sum = image_sum.rename("Emis29_31_32");
    image_sum = image_sum.set("system:time_start", time_start);
    return image_sum;
  })
  var imgCol_emissivity = imgCol_emissivity.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  })
  
  
  
  var bandName = 12*(year-2001)+month-9
  bandName = 'b' + bandName
  var img_incoming_shorRD = IncomingSR.select(bandName)
  var img_incoming_longRD = IncomingLR.select(bandName);

  var doyList = ee.List(imgCol_albedo.aggregate_array('doy'));
  var imgCol_snowmelt_rad = doyList.map(function(doy){
                                    var img_temp = imgCol_temp.filter(ee.Filter.eq('doy', doy)).first();
                                    var img_LST = imgCol_LST.filter(ee.Filter.eq('doy', doy)).first();
                                    var img_F = image_F;
                                    var img_albedo = imgCol_albedo.filter(ee.Filter.eq('doy', doy)).first();
                                    var img_emissivity = imgCol_emissivity.filter(ee.Filter.eq('doy', doy)).first();
                                    var img_1_minus_F = img_F.multiply(-1);
                                    var img_1_minus_F = img_1_minus_F.add(1);
                                    var img_1_minus_albedo = img_albedo.multiply(-1);
                                    var img_1_minus_albedo = img_1_minus_albedo.add(1);
                                    
                                    var img_snowmelt_shortRD = img_F.multiply(img_1_minus_albedo).multiply(img_incoming_shorRD);
                                    var img_snowmelt_longRD_air = img_F.multiply(img_emissivity).multiply(img_incoming_longRD);
                                    var img_snowmelt_longRD_canopy = img_1_minus_F.multiply(0.98).multiply(1e-8*5.67).multiply(img_temp).multiply(img_temp).multiply(img_temp).multiply(img_temp);
                                    var img_snowmelt_longRD_ref = img_emissivity.multiply(1e-8*5.67).multiply(img_LST).multiply(img_LST).multiply(img_LST).multiply(img_LST);
                                    var img_snowmelt_rad = img_snowmelt_shortRD.add(img_snowmelt_longRD_air).add(img_snowmelt_longRD_canopy).subtract(img_snowmelt_longRD_ref);
                                    img_snowmelt_rad = img_snowmelt_rad.multiply(0.026)
                                    var mask = img_snowmelt_rad.gt(0);
                                    var img_snowmelt_rad = img_snowmelt_rad.updateMask(mask);
                                    var img_snowmelt_rad = img_snowmelt_rad.set('doy', doy);
                                    return img_snowmelt_rad
                                  })
  var imgCol_snowmelt_rad = ee.ImageCollection.fromImages(imgCol_snowmelt_rad);
  var img_snowmelt_rad = imgCol_snowmelt_rad.sum() // unit: cm/month
  img_snowmelt_rad = img_snowmelt_rad.rename('snowmelt_rad_LST')
  return img_snowmelt_rad
  
}


function getSnowmelt_rad_LST_LE_SH(year, month, start, finish) {
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  


  var bandName = "Lai_500m"
  var bandName2 = "skyView"
  var Scale = 0.1;
  var unit = 'Leaf Area Index: sq. meter/sq. meter (per month)'
  var ImageCol_lai = LAICol.filterDate(startDate, endDate);
  // var ImageCol_lai = getMosaicImageCol(ImageCol_lai, startDate, endDate);
  var ImageCol_lai = ImageCol_lai.select(bandName);
  var imgCol_F = ImageCol_lai.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image_F = image.multiply(-0.5);
    var image_F = image_F.exp();
    image_F = image_F.rename(bandName2)
    image_F = image_F.set("system:time_start", time_start);
    return image_F;
  })
  var image_F = imgCol_F.mean()
  
  var bandName = "LST_Day_1km"
  var bandName2 = "LST_MODIS"
  var Scale = 0.02;
  var unit = 'Land Surface Temperature: K'
  var imgCol_LST = MODIS_LST.filterDate(startDate, endDate);
  // var imgCol_LST = getMosaicImageCol(imgCol_LST, start, finish);
  var imgCol_LST = imgCol_LST.select(["LST_Day_1km","LST_Night_1km"]);
  imgCol_LST = imgCol_LST.map(function(image){
    var time_start = image.get("system:time_start");
    var image_1 = image.select("LST_Day_1km");
    var image_2 = image.select("LST_Night_1km");
    var image_mean = image_1.add(image_2).divide(2);
    image_mean = image_mean.multiply(Scale).toDouble();
    image_mean = image_mean.rename(bandName2);
    image_mean = image_mean.set("system:time_start", time_start);
    return image_mean;
  })
  var imgCol_LST = imgCol_LST.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  });
  
  
  // var bandName = 'temperature_2m';
  // var unit = 'K';
  // var imgCol = getDailyData_mean(ERA5, start, finish, bandName);
  // var imgCol_temp = imgCol.map(function(image){
  //   var time_start = image.get("system:time_start");
  //   image = image.toDouble();
  //   image = image.rename(bandName)
  //   image = image.set("system:time_start", time_start);
  //   return image;
  // });
  //   var imgCol_temp = imgCol_temp.map(function(img) {
  // var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  // return img.set('doy', doy);
  // });

  var imgCol_temp  = imgCol_LST
  
  var bandName = "Albedo_WSA_shortwave"
  var bandName2 = "Albedo_WSA_shortwave_MODIS"
  var Scale = 0.001;
  var unit = 'Albedo percentage: 1, not %'
  var imgCol_albedo = MODIS_albedo.filterDate(startDate, endDate);
  // var imgCol_albedo = getMosaicImageCol(imgCol_albedo, start, finish);
  var imgCol_albedo = imgCol_albedo.select(bandName);
  imgCol_albedo = imgCol_albedo.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.rename(bandName2)
    image = image.set("system:time_start", time_start);
    return image;
  })
  var imgCol_albedo = imgCol_albedo.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  });
  
 
  var bandName = "Emis_31"
  var bandName2 = "Emis_32"
  var Col = MODIS_LST;
  var Scale = 0.002;
  if (month<10) {
  var EMS29 = ee.Image("users/yunxiaz1/MYD11C3_emissiivity_29/"+"EMS"+year+'0'+month);
  }
  if (month>9) {
  var EMS29 = ee.Image("users/yunxiaz1/MYD11C3_emissiivity_29/"+"EMS"+year+month);
  }
  var ImageCol = Col.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(["Emis_31","Emis_32"]);
  imgCol_emissivity = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    var image_1 = image.select("Emis_31");
    var image_2 = image.select("Emis_32");
    var image_sum = image_1.add(image_2);
    image_sum = image_sum.add(EMS29);
    image_sum = image_sum.multiply(Scale).toDouble();
    image_sum = image_sum.toDouble();
    image_sum = image_sum.rename("Emis29_31_32");
    image_sum = image_sum.set("system:time_start", time_start);
    return image_sum;
  })
  var imgCol_emissivity = imgCol_emissivity.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  })
  
  var bandName = "LE"
  var bandName2 = "LE_MODIS"
  var Scale = 10000;
  var unit = 'Average MODIS LE: W/m2'
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = MODIS_ET.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(bandName);
  
  var imgCol_LE = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.divide(24).divide(60).divide(60).toDouble();
    image = image.rename('le')
    image = image.set("system:time_start", time_start);
    return image;
  })
  var imgCol_LE = imgCol_LE.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  })
  
  
  var bandName = 'surface_sensible_heat_flux';
  var unit = 'J/m2';
  var imgCol = getDailyData_sum(ERA5, start, finish, bandName);
  var imgCol_SE = imgCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.toDouble();
    image = image.divide(24).divide(60).divide(60).toDouble();
    image = image.rename(bandName)
    image = image.set("system:time_start", time_start);
    return image;
  });
  var imgCol_SE = imgCol_SE.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  });
  
  
  var bandName = 12*(year-2001)+month-9
  bandName = 'b' + bandName
  var img_incoming_shorRD = IncomingSR.select(bandName)
  var img_incoming_longRD = IncomingLR.select(bandName);



  var doyList = ee.List(imgCol_albedo.aggregate_array('doy'));
  var imgCol_snowmelt_rad = doyList.map(function(doy){
                                    
                                    var img_temp = imgCol_temp.filter(ee.Filter.eq('doy', doy)).first();
                                    
                                    var doy = ee.Date(img_temp.get('system:time_start')).getRelative('day', 'year');
                                    var img_le = imgCol_LE.mean();
                                    img_le = img_le.set('doy', doy);
                                    var img_se = imgCol_SE.mean();
                                    img_se = img_se.set('doy', doy);
                                    
                                    var img_LST = imgCol_LST.filter(ee.Filter.eq('doy', doy)).first();
                                    var img_F = image_F;
                                    var img_albedo = imgCol_albedo.filter(ee.Filter.eq('doy', doy)).first();
                                    var img_emissivity = imgCol_emissivity.filter(ee.Filter.eq('doy', doy)).first();
                                    var img_1_minus_F = img_F.multiply(-1);
                                    var img_1_minus_F = img_1_minus_F.add(1);
                                    var img_1_minus_albedo = img_albedo.multiply(-1);
                                    var img_1_minus_albedo = img_1_minus_albedo.add(1);
                                    
                                    var img_snowmelt_shortRD = img_F.multiply(img_1_minus_albedo).multiply(img_incoming_shorRD);
                                    var img_snowmelt_longRD_air = img_F.multiply(img_emissivity).multiply(img_incoming_longRD);
                                    var img_snowmelt_longRD_canopy = img_1_minus_F.multiply(0.98).multiply(1e-8*5.67).multiply(img_temp).multiply(img_temp).multiply(img_temp).multiply(img_temp);
                                    var img_snowmelt_longRD_ref = img_emissivity.multiply(1e-8*5.67).multiply(img_LST).multiply(img_LST).multiply(img_LST).multiply(img_LST);
                                    var img_snowmelt_rad = img_snowmelt_shortRD.add(img_snowmelt_longRD_air).add(img_snowmelt_longRD_canopy).subtract(img_snowmelt_longRD_ref);
                                    var img_snowmelt_rad = img_snowmelt_rad.add(img_le).add(img_se)
                                    img_snowmelt_rad = img_snowmelt_rad.multiply(0.026)
                                    var mask = img_snowmelt_rad.gt(0);
                                    var img_snowmelt_rad = img_snowmelt_rad.updateMask(mask);
                                    var img_snowmelt_rad = img_snowmelt_rad.set('doy', doy);
                                    return img_snowmelt_rad
                                  })
  var imgCol_snowmelt_rad = ee.ImageCollection.fromImages(imgCol_snowmelt_rad);
  var img_snowmelt_rad = imgCol_snowmelt_rad.sum() // unit: cm/month
  img_snowmelt_rad = img_snowmelt_rad.rename('snowmelt_rad_LST_LE_SH')
  return img_snowmelt_rad
  
}


function getSnowmelt_rad_temp_LE_HE(year, month, start, finish) {
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  


  var bandName = "Lai_500m"
  var bandName2 = "skyView"
  var Scale = 0.1;
  var unit = 'Leaf Area Index: sq. meter/sq. meter (per month)'
  var ImageCol_lai = LAICol.filterDate(startDate, endDate);
  // var ImageCol_lai = getMosaicImageCol(ImageCol_lai, startDate, endDate);
  var ImageCol_lai = ImageCol_lai.select(bandName);
  var imgCol_F = ImageCol_lai.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image_F = image.multiply(-0.5);
    var image_F = image_F.exp();
    image_F = image_F.rename(bandName2)
    image_F = image_F.set("system:time_start", time_start);
    return image_F;
  })
  var image_F = imgCol_F.mean()
  

  
  
  var bandName = 'temperature_2m';
  var unit = 'K';
  var imgCol = getDailyData_mean(ERA5, start, finish, bandName);
  var imgCol_temp = imgCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.toDouble();
    image = image.rename(bandName)
    image = image.set("system:time_start", time_start);
    return image;
  });
    var imgCol_temp = imgCol_temp.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  });


  var bandName = 'surface_sensible_heat_flux';
  var unit = 'J/m2';
  var imgCol = getDailyData_sum(ERA5, start, finish, bandName);
  var imgCol_SE = imgCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.toDouble();
    image = image.divide(24).divide(60).divide(60).toDouble();
    image = image.rename(bandName)
    image = image.set("system:time_start", time_start);
    return image;
  });
  var imgCol_SE = imgCol_SE.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  });
  
  
  
  var bandName = "Albedo_WSA_shortwave"
  var bandName2 = "Albedo_WSA_shortwave_MODIS"
  var Scale = 0.001;
  var unit = 'Albedo percentage: 1, not %'
  var imgCol_albedo = MODIS_albedo.filterDate(startDate, endDate);
  // var imgCol_albedo = getMosaicImageCol(imgCol_albedo, start, finish);
  var imgCol_albedo = imgCol_albedo.select(bandName);
  imgCol_albedo = imgCol_albedo.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.rename(bandName2)
    image = image.set("system:time_start", time_start);
    return image;
  })
  var imgCol_albedo = imgCol_albedo.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  });
  
 
  var bandName = "Emis_31"
  var bandName2 = "Emis_32"
  var Col = MODIS_LST;
  var Scale = 0.002;
  if (month<10) {
  var EMS29 = ee.Image("users/yunxiaz1/MYD11C3_emissiivity_29/"+"EMS"+year+'0'+month);
  }
  if (month>9) {
  var EMS29 = ee.Image("users/yunxiaz1/MYD11C3_emissiivity_29/"+"EMS"+year+month);
  }
  var ImageCol = Col.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(["Emis_31","Emis_32"]);
  imgCol_emissivity = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    var image_1 = image.select("Emis_31");
    var image_2 = image.select("Emis_32");
    var image_sum = image_1.add(image_2);
    image_sum = image_sum.add(EMS29);
    image_sum = image_sum.multiply(Scale).toDouble();
    image_sum = image_sum.toDouble();
    image_sum = image_sum.rename("Emis29_31_32");
    image_sum = image_sum.set("system:time_start", time_start);
    return image_sum;
  })
  var imgCol_emissivity = imgCol_emissivity.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  })
  
  var bandName = "LE"
  var bandName2 = "LE_MODIS"
  var Scale = 10000;
  var unit = 'Average MODIS LE: W/m2'
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = MODIS_ET.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(bandName);
  
  var imgCol_LE = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.divide(24).divide(60).divide(60).toDouble();
    image = image.rename('le')
    image = image.set("system:time_start", time_start);
    return image;
  })
  var imgCol_LE = imgCol_LE.map(function(img) {
  var doy = ee.Date(img.get('system:time_start')).getRelative('day', 'year');
  return img.set('doy', doy);
  })
  
  
  
  var bandName = 12*(year-2001)+month-9
  bandName = 'b' + bandName
  var img_incoming_shorRD = IncomingSR.select(bandName)
  var img_incoming_longRD = IncomingLR.select(bandName);



  var doyList = ee.List(imgCol_albedo.aggregate_array('doy'));
  var imgCol_snowmelt_rad = doyList.map(function(doy){
                                    
                                    var img_temp = imgCol_temp.filter(ee.Filter.eq('doy', doy)).first();
                                    
                                    var doy = ee.Date(img_temp.get('system:time_start')).getRelative('day', 'year');
                                    var img_le = imgCol_LE.mean();
                                    img_le = img_le.set('doy', doy);
                                    
                                    var img_se = imgCol_SE.mean();
                                    img_se = img_se.set('doy', doy);
                                    
                                    var img_LST = img_temp;
                                    var img_F = image_F;
                                    var img_albedo = imgCol_albedo.filter(ee.Filter.eq('doy', doy)).first();
                                    var img_emissivity = imgCol_emissivity.filter(ee.Filter.eq('doy', doy)).first();
                                    var img_1_minus_F = img_F.multiply(-1);
                                    var img_1_minus_F = img_1_minus_F.add(1);
                                    var img_1_minus_albedo = img_albedo.multiply(-1);
                                    var img_1_minus_albedo = img_1_minus_albedo.add(1);
                                    
                                    var img_snowmelt_shortRD = img_F.multiply(img_1_minus_albedo).multiply(img_incoming_shorRD);
                                    var img_snowmelt_longRD_air = img_F.multiply(img_emissivity).multiply(img_incoming_longRD);
                                    var img_snowmelt_longRD_canopy = img_1_minus_F.multiply(0.98).multiply(1e-8*5.67).multiply(img_temp).multiply(img_temp).multiply(img_temp).multiply(img_temp);
                                    var img_snowmelt_longRD_ref = img_emissivity.multiply(1e-8*5.67).multiply(img_LST).multiply(img_LST).multiply(img_LST).multiply(img_LST);
                                    var img_snowmelt_rad = img_snowmelt_shortRD.add(img_snowmelt_longRD_air).add(img_snowmelt_longRD_canopy).subtract(img_snowmelt_longRD_ref);
                                    var img_snowmelt_rad = img_snowmelt_rad.add(img_le).add(img_se)
                                    img_snowmelt_rad = img_snowmelt_rad.multiply(0.026)
                                    var mask = img_snowmelt_rad.gt(0);
                                    var img_snowmelt_rad = img_snowmelt_rad.updateMask(mask);
                                    var img_snowmelt_rad = img_snowmelt_rad.set('doy', doy);
                                    return img_snowmelt_rad
                                  })
  var imgCol_snowmelt_rad = ee.ImageCollection.fromImages(imgCol_snowmelt_rad);
  var img_snowmelt_rad = imgCol_snowmelt_rad.sum() // unit: cm/month
  img_snowmelt_rad = img_snowmelt_rad.rename('snowmelt_rad_temp_LE_HE')
  return img_snowmelt_rad
  
}


// the first/last day there is(not) snow compared to sdate
function getHasSnowDayYearImage(year, month) {
  year = ee.Number(year).toInt();
  if (month < 10 ) {
  var sdate = ee.Date.fromYMD(year.subtract(1), 10, 1);
  var edate = ee.Date.fromYMD(year, 10, 1); 
  } 
  if (month > 9 ) {
  var sdate = ee.Date.fromYMD(year, 10, 1);
  var edate = ee.Date.fromYMD(year.add(1), 10, 1); 
  }   
  
  
  

  var yearImgCol = snowCover.filterDate(sdate, edate)
                           .select("NDSI_Snow_Cover")
                           .map(function(image) {
                             var time_start = image.get("system:time_start");
                             var mask = image.gt(0);
                             mask = mask.set("system:time_start", time_start);
                             return mask;
                           });
  var idList = yearImgCol.reduceColumns(ee.Reducer.toList(), ["system:index"])
                         .get("list");
  idList = ee.List(idList);
  var indexList = ee.List.sequence(2, idList.size().subtract(2));
  // print(indexList)
  idList = indexList.map(function(index) {
    index = ee.Number(index);
    var subIndexList = ee.List.sequence(index.subtract(2), index);
    var subIdList = subIndexList.map(function(subIndex) {
      subIndex = ee.Number(subIndex);
      return idList.get(subIndex);
    });
    return subIdList;
  });

  // print(idList)
  var dayImgList = idList.iterate(function(ids, list) {
    ids = ee.List(ids);
    list = ee.List(list);
    var dayImg = yearImgCol.filter(ee.Filter.inList("system:index", ids))
                           .sum();
    var mask = dayImg.eq(3);
    var curDate = ee.Date.parse("yyyy_MM_dd", ids.get(1));
    var day = curDate.difference(sdate, "day");
    var dateImg = ee.Image.constant(day.add(1)).updateMask(mask);
    dateImg = dateImg.rename("day").toInt();
    dateImg = dateImg.set("system:time_start", curDate.millis());
    dateImg = dateImg.set("system:index", curDate.format("yyyy_MM_dd"));
    return list.add(dateImg);
  }, ee.List([]));
  
  // print(dayImgList)
  var dayImgCol = ee.ImageCollection.fromImages(ee.List(dayImgList));
  var lastDayImg = dayImgCol.mosaic();
  var firstDayImg = dayImgCol.sort("system:time_start", false).mosaic();
  var yearImg = firstDayImg.rename("first_snow")
                           .addBands(lastDayImg.rename("last_snow"));
  yearImg = yearImg.set("year", year);
  yearImg = yearImg.set("system:time_start", sdate.millis());
  yearImg = yearImg.set("system:index", sdate.format("yyyy_MM_dd"));
  // print(yearImg)
  return yearImg.toInt();
}





function getNetRadiation_MODIS_snow_LST(year, month, start, finish) {
  var image_LST = getLST_MODIS(start, finish); 
  var image_LST = image_LST.add(273.15).toDouble();
  var image_lai = getLAI_MODIS(start, finish);
  image_lai = image_lai.multiply(-0.5);
  var img_F = image_lai.exp();
  
  var image_net_short_rad = getNetShortRadiation_MODIS(year, month, start, finish);
  image_net_short_rad = image_net_short_rad.multiply(img_F);
  var image_long_Rad_surface = getReflected_LongRadiation_MODIS(year, month, start, finish);
  
  var image_emis = getEM29_31_32_MODIS(year, month, start, finish);
  var bandName = 12*(year-2001)+month-9;
  bandName = 'b' + bandName;
  var image_RD = IncomingLR.select(bandName);
  var image_net_long_Rad_air = image_RD.multiply(image_emis).multiply(img_F);
  
  var image_long_Rad_canopy = img_F.multiply(-1);
  image_long_Rad_canopy = image_long_Rad_canopy.add(1);
  image_long_Rad_canopy = image_long_Rad_canopy.multiply(0.98);
  image_long_Rad_canopy = image_long_Rad_canopy.multiply(image_LST).multiply(image_LST).multiply(image_LST).multiply(image_LST);
  image_long_Rad_canopy = image_long_Rad_canopy.multiply(1e-8*5.67)
  
  var image_netRad_snow = image_net_long_Rad_air.add(image_long_Rad_canopy).add(image_net_short_rad).add(image_long_Rad_surface)
  return image_netRad_snow.rename('net_Rad_snow_LST');
}


function getNetRadiation_MODIS_snow(year, month, start, finish) {
  var image_temp = getTemp_ERA5(start, finish);
  image_temp = image_temp.add(273.25).toDouble();
  var image_lai = getLAI_MODIS(start, finish);
  image_lai = image_lai.multiply(-0.5);
  var img_F = image_lai.exp();
  
  var image_net_short_rad = getNetShortRadiation_MODIS(year, month, start, finish);
  image_net_short_rad = image_net_short_rad.multiply(img_F);
  var image_long_Rad_surface = getReflected_LongRadiation_MODIS(year, month, start, finish);
  var image_emis = getEM29_31_32_MODIS(year, month, start, finish);
  var bandName = 12*(year-2001)+month-9;
  bandName = 'b' + bandName;
  var image_RD = IncomingLR.select(bandName);
  var image_net_long_Rad_air = image_RD.multiply(image_emis).multiply(img_F);
  var image_long_Rad_canopy = img_F.multiply(-1);
  image_long_Rad_canopy = image_long_Rad_canopy.add(1);
  image_long_Rad_canopy = image_long_Rad_canopy.multiply(0.98);
  image_long_Rad_canopy = image_long_Rad_canopy.multiply(image_temp).multiply(image_temp).multiply(image_temp).multiply(image_temp);
  image_long_Rad_canopy = image_long_Rad_canopy.multiply(1e-8*5.67)
  var image_netRad_snow = image_net_short_rad.add(image_net_long_Rad_air).add(image_long_Rad_canopy).add(image_long_Rad_surface)
  return image_netRad_snow.rename('net_Rad_snow');
}



function getNetShortRadiation_MODIS(year, month, start, finish) {
  var bandName = 12*(year-2001)+month-9
  bandName = 'b' + bandName
  var image_RD = IncomingSR.select(bandName)
  var image_albedo = getAlbedo_MODIS(start, finish)
  var image_net_RD = image_RD.multiply(image_albedo)
  var image_net_short_RD = image_RD.subtract(image_net_RD)
  var img = image_net_short_RD.rename('net_short_Rad');
  return img;
}

function getReflected_LongRadiation_MODIS(year, month, start, finish) {
  var image_emis = getEM29_31_32_MODIS(year, month, start, finish);
  var image_LST = getLST_MODIS(start, finish); 
  var image_LST = image_LST.add(273.15).toDouble();
  var image_net_long_RD = image_LST.multiply(image_LST).multiply(image_LST).multiply(image_LST);
  image_net_long_RD = image_net_long_RD.multiply(-1e-8*5.67);
  image_net_long_RD = image_net_long_RD.multiply(image_emis);
  var img = image_net_long_RD.rename('ref_long_Rad');
  return img;
  
}


function getNetLongRadiation_MODIS(year, month, start, finish) {
  var image_emis = getEM29_31_32_MODIS(year, month, start, finish);
  
  var bandName = 12*(year-2001)+month-9
  bandName = 'b' + bandName
  var image_RD = IncomingLR.select(bandName);
  image_RD = image_RD.multiply(image_emis)
  
  var image_LST = getLST_MODIS(start, finish); 
  var image_LST = image_LST.add(273.15).toDouble();
  var image_net_long_RD = image_LST.multiply(image_LST).multiply(image_LST).multiply(image_LST);
  image_net_long_RD = image_net_long_RD.multiply(-1e-8*5.67);
  image_net_long_RD = image_net_long_RD.multiply(image_emis);
  image_net_long_RD = image_net_long_RD.add(image_RD);
  var img = image_net_long_RD.rename('net_long_Rad');
  return img;
  return image_emis.rename('net_long_Rad');
}

function getNetRadiation_MODIS(year, month, start, finish) {
  var image_net_long_RD = getNetLongRadiation_MODIS(year, month, start, finish);
  var image_net_short_RD = getNetShortRadiation_MODIS(year, month, start, finish);
  var image_net_RD = image_net_long_RD.add(image_net_short_RD);
  var img = image_net_RD.rename('net_Rad');
  return img;
}

function getEM29_31_32_MODIS(year, month, start, finish) {
  var Col = MODIS_LST;
  var bandName = "Emis_31"
  var bandName2 = "Emis_32"
  var Scale = 0.002;
  
  if (month<10) {
  var EMS29 = ee.Image("users/yunxiaz1/MYD11C3_emissiivity_29/"+"EMS"+year+'0'+month);
  }
  if (month>9) {
  var EMS29 = ee.Image("users/yunxiaz1/MYD11C3_emissiivity_29/"+"EMS"+year+month);
  }
  
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = Col.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(["Emis_31","Emis_32"]);
  var imgCol = null;
  imgCol = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    var image_1 = image.select("Emis_31");
    var image_2 = image.select("Emis_32");
    var image_sum = image_1.add(image_2);
    image_sum = image_sum.add(EMS29);
    image_sum = image_sum.multiply(Scale).toDouble();
    image_sum = image_sum.toDouble();
    image_sum = image_sum.set("system:time_start", time_start);
    return image_sum;
  })
  var img = imgCol.mean().rename("Emis29_31_32");

  return img;
}




// *********************************** Get Daily Value ******************************************************

function day_mosaics(date, newlist, rawImgCol) {
  // Cast
  date = ee.Date(date);
  newlist = ee.List(newlist);
  // Filter collection between date and the next day
  var filtered = rawImgCol.filterDate(date, date.advance(1,'day'));
  // Make the mosaic
  var image = ee.Image(filtered.mosaic());
  image = image.set("system:time_start", date.format("yyyyMMdd"));
  image = image.set("system:index", date.format("yyyy_MM_dd"));
  image = image.set("count", filtered.size());
  // Add the mosaic to a list only if the collection has images
  return ee.List(ee.Algorithms.If(filtered.size(), newlist.add(image), newlist));
}
function getMosaicImageCol(imgCol, startDate, endDate) {
  endDate = ee.Date(endDate);
  startDate = ee.Date(startDate);
  var ImageCol = imgCol.filter(ee.Filter.date(startDate, endDate));
  var diff = endDate.difference(startDate, 'day');
  // Make a list of all dates
  var range = ee.List.sequence(0, diff.subtract(1))
                .map(function(day){
                  return startDate.advance(day,'day');
                }); 
  // Iterate over the range to make a new list, and then cast the list to an imagecollection
  var ImageColList = range.iterate(function(date, newlist) {
    return day_mosaics(date, newlist, ImageCol);
  }, ee.List([]));
  var MosaicImageCol = ee.ImageCollection(ee.List(ImageColList))
                         .filter(ee.Filter.gt("count", 0));
  return MosaicImageCol;
}

function getDailyData_sum(Col, start, finish, bandName) {
  start = ee.Date(start); // set start time for analysis
  finish = ee.Date(finish); // set end time for analysis
  var nDays = ee.Number(finish.difference(start,'day')).round();// calculate the number of days to process
  var is = Col.select(bandName).filterDate(start, finish);
  var list = // map over each month
    ee.List.sequence(0,nDays.subtract(1)).map(function (n) {
      // calculate the offset from startDate
      var ini = start.advance(n,'day');
      // advance just one month
      var end = ini.advance(1,'day');
      // filter and reduce
      var _temp = is.filterDate(ini,end)
                    .select(bandName);
      return _temp.reduce(ee.Reducer.sum())
                  .toDouble()
                  .rename(bandName)
                  .set('system:time_start', ini.millis())
                  .set("count", _temp.size());
  });

  var byDay = ee.ImageCollection(list).filter(ee.Filter.gt("count", 0));
  
  return byDay.filterDate(start, finish);
}




function getDailyData_mean(Col, start, finish, bandName) {
  start = ee.Date(start); // set start time for analysis
  finish = ee.Date(finish); // set end time for analysis
  var nDays = ee.Number(finish.difference(start,'day')).round();// calculate the number of days to process
  var is = Col.select(bandName).filterDate(start, finish);
  var list = // map over each month
    ee.List.sequence(0,nDays.subtract(1)).map(function (n) {
      // calculate the offset from startDate
      var ini = start.advance(n,'day');
      // advance just one month
      var end = ini.advance(1,'day');
      // filter and reduce
      var _temp = is.filterDate(ini,end)
                    .select(bandName);
      return _temp.reduce(ee.Reducer.mean())
                  .toDouble()
                  .rename(bandName)
                  .set('system:time_start', ini.millis())
                  .set("count", _temp.size());
  });
  var byDay = ee.ImageCollection(list).filter(ee.Filter.gt("count", 0));
  return byDay.filterDate(start, finish);
}


function getTemp_ERA5(start, finish){
  var bandName = 'temperature_2m';
  var unit = 'degree';
  
  var Col = ERA5
  var imgCol = getDailyData_mean(Col, start, finish, bandName);
  
  var imgCol2 = null;
  imgCol2 = imgCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.subtract(273.15).toDouble();
    image = image.set("system:time_start", time_start);
    return image;
  });
  var img = imgCol2.mean().rename('temp_era5');
  return img;
}


function getSH_ERA5(start, finish){
  var bandName = 'surface_sensible_heat_flux';
  var unit = 'W/m2';
  
  var Col = ERA5
  var imgCol = getDailyData_sum(Col, start, finish, bandName);
  
  var imgCol2 = null;
  imgCol2 = imgCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.toDouble();
    image = image.divide(24).divide(60).divide(60).toDouble();
    image = image.set("system:time_start", time_start);
    return image;
  });
  var img = imgCol2.mean().rename('SH_ERA5');
  return img;
}





function getSnowmelt_ERA5(start, finish){
  var bandName = 'snowmelt_hourly';
  var unit = 'm of water equivalent';
  
  var Col = ERA5
  var imgCol = getDailyData_sum(Col, start, finish, bandName);
  
  var imgCol2 = null;
  imgCol2 = imgCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.toDouble();
    image = image.set("system:time_start", time_start);
    return image;
  });
  var img = imgCol2.sum().rename('snowmelt');
  return img;
}

function getPrecip_MODIS(start, finish) {
  var bandName = 'precipitationCal';
  var bandName2 = 'Precip_MODIS';
  var Scale = 0.5;
  var unit = 'mm/month'
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = MODIS_precip.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(bandName);
  var imgCol = null;
  imgCol = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.set("system:time_start", time_start);
    return image;
  })
  var img = imgCol.sum().rename(bandName2);
  return img;
}

function getNDVI_MODIS(start, finish) {
  var bandName = 'NDVI';
  var bandName2 = 'NDVI';
  var Scale = 0.0001;
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = MODIS_veg.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(bandName);
  var imgCol = null;
  imgCol = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.set("system:time_start", time_start);
    return image;
  })
  var img = imgCol.mean().rename(bandName2);
  return img;
}

function getEVI_MODIS(start, finish) {
  var bandName = 'EVI';
  var bandName2 = 'EVI';
  var Scale = 0.0001;
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = MODIS_veg.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(bandName);
  var imgCol = null;
  imgCol = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.set("system:time_start", time_start);
    return image;
  })
  var img = imgCol.mean().rename(bandName2);
  return img;
}

function getLAI_MODIS(start, finish) {
  var Col = LAICol;
  var bandName = "Lai_500m"
  var bandName2 = "Lai"
  var Scale = 0.1;
  var unit = 'Leaf Area Index: sq. meter/sq. meter (per month)'
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = Col.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(bandName);
  var imgCol = null;
  imgCol = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.set("system:time_start", time_start);
    return image;
  })
  var img = imgCol.mean().rename(bandName2);
  return img;
}
function getLandCover_MODIS(start, finish) {
  var Col = MODIS_LandCover;
  var bandName = "LC_Type1"
  var bandName2 = "LC_Type1_MODIS"
  var Scale = 1;
  var unit = 'Land Cover Type 1: Annual International Geosphere-Biosphere Programme (IGBP) classification'
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = Col.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(bandName);
  var imgCol = null;
  imgCol = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.set("system:time_start", time_start);
    return image;
  })
  var img = imgCol.mean()
  img = img.rename(bandName2);
  return img;
}

function getET_MODIS(start, finish) {
  // var Col = MODIS_ET2;
  var bandName = "ET"
  var bandName2 = "ET_MODIS"
  var Scale = 0.1;
  var unit = 'Total MODIS evapotranspiration: kg/m^2(per month)'
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = MODIS_ET.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(bandName);
  var imgCol = null;
  imgCol = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.set("system:time_start", time_start);
    return image;
  })
  var img = imgCol.sum().rename(bandName2);
  return img;
}

function getLE_MODIS(start, finish){
  var bandName = "LE"
  var bandName2 = "LE_MODIS"
  var Scale = 10000;
  var unit = 'Average MODIS LE: W/m2'
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = MODIS_ET.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(bandName);
  var imgCol = null;
  imgCol = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.divide(24).divide(60).divide(60).toDouble();
    image = image.set("system:time_start", time_start);
    return image;
  })
  var img = imgCol.mean().rename(bandName2);
  return img;
}



function getPET_MODIS(start, finish) {
  // var Col = MODIS_ET2;
  var bandName = "PET"
  var bandName2 = "PET_MODIS"
  var Scale = 0.1;
  var unit = 'Total MODIS potential evapotranspiration: kg/m^2(per month)'
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = MODIS_ET.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(bandName);
  var imgCol = null;
  imgCol = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.set("system:time_start", time_start);
    return image;
  })
  var img = imgCol.sum().rename(bandName2);
  return img;
}

function getSnowAlbedo_MODIS(start, finish) {
  var Col = snowCover;
  var bandName = "Snow_Albedo_Daily_Tile"
  var bandName2 = "Snow_Albedo"
  var Scale = 0.01;
  var unit = 'Snow albedo percentage: 1, not %'
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = Col.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(bandName);
  var imgCol = null;
  imgCol = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.set("system:time_start", time_start);
    return image;
  })
  var img = imgCol.mean().rename(bandName2);
  return img;
}
function getSnowCoverage_MODIS(start, finish) {
  var Col = snowCover;
  var bandName = "NDSI_Snow_Cover"
  var bandName2 = "NDSI_Snow_Cover_MODIS"
  var Scale = 0.01;
  var unit = 'NDSI snow cover: 1, not %'
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = Col.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(bandName);
  var imgCol = null;
  imgCol = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.set("system:time_start", time_start);
    return image;
  })
  var img = imgCol.mean().rename(bandName2);
  return img;
}
function getAlbedo_MODIS(start, finish) {
  var Col = MODIS_albedo;
  var bandName = "Albedo_WSA_shortwave"
  var bandName2 = "Albedo_WSA_shortwave_MODIS"
  var Scale = 0.001;
  var unit = 'Albedo percentage: 1, not %'
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = Col.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(bandName);
  var imgCol = null;
  imgCol = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    image = image.multiply(Scale).toDouble();
    image = image.set("system:time_start", time_start);
    return image;
  })
  var img = imgCol.mean().rename(bandName2);
  return img;
}
function getLST_MODIS(start, finish) {
  var Col = MODIS_LST;
  var bandName = "LST_Day_1km"
  var bandName2 = "LST_MODIS"
  var Scale = 0.02;
  var unit = 'Daytime Land Surface Temperature: celcius degree'
  var startDate = ee.Date(start);
  var endDate = ee.Date(finish);
  var ImageCol = Col.filterDate(startDate, endDate);
  // var MosaicImageCol = getMosaicImageCol(ImageCol, start, finish);
  var MosaicImageCol = ImageCol.select(["LST_Day_1km","LST_Night_1km"]);
  var imgCol = null;
  imgCol = MosaicImageCol.map(function(image){
    var time_start = image.get("system:time_start");
    var image_1 = image.select("LST_Day_1km");
    var image_2 = image.select("LST_Night_1km");
    var image_mean = image_1.add(image_2).divide(2);
    image_mean = image_mean.multiply(Scale).subtract(273.15).toDouble();
    image_mean = image_mean.set("system:time_start", time_start);
    return image_mean;
  })
  var img = imgCol.mean().rename(bandName2);
  return img;
}


// ********************************************************** Extract Data by Region *******************************************************************************************


var getGeometry1 = function(feature) {
        // var keepProperties = ['id', 'BurnDate', 'lat', 'lon', 'ObjectID'];
        var keepProperties = ['index', 'BurnDate', 'latitude', 'longitude'];
        var geometry = ee.Geometry.Point([ feature.get('longitude'), feature.get('latitude')]);
        return ee.Feature(geometry).copyProperties(feature, keepProperties);
    };

var getGeometry2 = function(feature) {
        // var keepProperties = ['id', 'BurnDate', 'lat', 'lon', 'ObjectID'];
        var keepProperties = ['ObjectID', 'lon', 'lat'];
        var geometry = ee.Geometry.Point([ feature.get('lon'), feature.get('lat')]);
        return ee.Feature(geometry).copyProperties(feature, keepProperties);
    };   
    
function imageToFeaCol(Burns){ 
  var fireImage = Burns.updateMask(Burns.select('BurnDate').mask())
  var dataDict = fireImage.reduceRegion({
  reducer: ee.Reducer.toList(),
  geometry: roi,
  scale: 1000,
  maxPixels: 1e13,
  tileScale: 16
  });
  var bandNames = fireImage.bandNames();
  var List_0 = ee.List(dataDict.get(bandNames.get(0)));
  var List_1 = ee.List(dataDict.get(bandNames.get(1)));
  var List_2 = ee.List(dataDict.get(bandNames.get(2)));
  var indexList = ee.List.sequence(0, List_0.length().subtract(1));
  var fList = indexList.map(function(index) {
      index = ee.Number(index).toInt();
      var feat =  ee.Feature(ee.Geometry.Point([List_1.get(index),List_2.get(index)]), {
        index: index,
        BurnDate: List_0.get(index),
        longitude: List_1.get(index),
        latitude: List_2.get(index),
      });
      return feat
    });
  var fcol = ee.FeatureCollection(fList);
  return fcol
}



function extractSnowTempRainAlbedo(featureCol, image, fileName, folderName, selectedVar) {
  var pFCol = featureCol.map(function(feature) {
    var pList = [feature];
    var tempCol = ee.FeatureCollection(ee.List(pList));
    return tempCol;
  });

  pFCol = pFCol.flatten();
  pFCol = image.reduceRegions({
    collection: pFCol,
    reducer: ee.Reducer.mean(),
    scale: 1000,
    tileScale: 16
  });
  // print(pFCol)
  Export.table.toDrive({
    collection: pFCol,
    description: fileName,
    folder:folderName,
    selectors: selectedVar,
    fileFormat: "CSV"
  });
  
//   image = image.clip(featureCol);
//   Export.image.toDrive({
//   image: image, 
//   description:fileName,
//   folder: folderName,
//   fileNamePrefix: fileName,
//   region: roi,
//   scale: 1000,
//   maxPixels: 1e13
//   });
  
}



    
// *********************************************************** Extract Value **************************************************************************************

function ExtractImgValue(image_burnID, featureCol, folderName, snowStartYear,snowEndYear,monthStart,monthEnd,fireYear) {
  
  for (var year=snowStartYear; year<=snowEndYear; year++) {
    for (var month=monthStart; month<=monthEnd; month++) {
      
      var fileName = "";
      // For LandCover, only Jan data is available. So for each water year, the IGBP is the same for each month!!
      if (month < 9 ) {
        fileName ='image_All_1km_'+year+'0' + month + '01to' +(year)+'0' + (month+1) + '01';
        var start = year+'-' + month + '-1';
        var finish = year+'-' + (month+1) + '-1';
        var start2 = year+'-1-1';
        var finish2 = year+'-2-1';
      } 
      if (month == 9 ) {
        fileName ='image_All_1km_'+year+'0' + month + '01to' +(year) + (month+1) + '01';
        var start = year+'-' + month + '-1';
        var finish = year+'-' + (month+1) + '-1';
        var start2 = year+'-1-1';
        var finish2 = year+'-2-1';
      } 
      if (month > 9 & month < 12) {
        fileName = 'image_All_1km_'+year + month + '01to' +(year) + (month+1) + '01' ;
        var start = year+'-' + month + '-1';
        var finish = year+'-' + (month+1) + '-1';
        var start2 = (year+1)+'-1-1';
        var finish2 = (year+1)+'-2-1';
      }
      if (month == 12) {
         fileName = 'image_All_1km_'+year + month + '01to' +(year+1)+'01'  + '01';
         var start = year+'-' + month + '-1';
         var finish = (year+1)+'-'  + '1-1';
        var start2 = (year+1)+'-1-1';
        var finish2 = (year+1)+'-2-1';
      }
      
      

      var image_getPrecip_MODIS = getPrecip_MODIS(start, finish)
      var image_getNDVI_MODIS = getNDVI_MODIS(start, finish)
      var image_getEVI_MODIS = getEVI_MODIS(start, finish)
      var image_getLAI_MODIS = getLAI_MODIS(start, finish)
      var image_getLandCover_MODIS = getLandCover_MODIS(start2, finish2)
      var image_getET_MODIS = getET_MODIS(start, finish)
      var image_getPET_MODIS = getPET_MODIS(start, finish)
      var image_LE = getLE_MODIS(start, finish) 
      var image_getSnowAlbedo_MODIS = getSnowAlbedo_MODIS(start, finish)
      var image_getSnowCoverage_MODIS = getSnowCoverage_MODIS(start, finish)
      var image_getAlbedo_MODIS = getAlbedo_MODIS(start, finish)
      var image_getLST_MODIS = getLST_MODIS(start, finish) 
      // var image_getIncomingShortRad_GLDAS = getIncomingShortRad_GLDAS(start, finish)
      var properties = ["BIOME_NUM", "ECO_ID"];
      var image_Biome = ecoRegions.reduceToImage({
                          properties: properties,
                          reducer: ee.Reducer.first().forEach(properties)
                        });
      image_Biome = image_Biome.select(["BIOME_NUM", "ECO_ID"])
      var basin = Basin.select('HYBAS_ID');
      var properties = ['HYBAS_ID']
      var image_Basin = basin.reduceToImage({
                          properties: properties,
                          reducer: ee.Reducer.first().forEach(properties)
                        });

      var image_net_short_RD = getNetShortRadiation_MODIS(year, month, start, finish) 
      
      var image_net_long_RD = getNetLongRadiation_MODIS(year, month, start, finish) 
      
      var image_net_RD = getNetRadiation_MODIS(year, month, start, finish)
      
      var image_snowmelt = getSnowmelt_ERA5(start, finish)
      
      var image_net_RD_snow = getNetRadiation_MODIS_snow(year, month, start, finish) 
      var image_temp_era5 = getTemp_ERA5(start, finish)
      
      
      var yearSnow = getHasSnowDayYearImage(year, month)
      var image_ref_longRD = getReflected_LongRadiation_MODIS(year, month, start, finish)
      var image_net_RD_snow_LST = getNetRadiation_MODIS_snow_LST(year, month, start, finish)
     
      var image_Accu_precip_snow = getAccu_precip_snow(year, month, start, finish)
      var image_Snowmelt_temp = getSnowmelt_temp(year, month, start, finish)
      var image_Snowmelt_rad = getSnowmelt_rad(year, month, start, finish)
      
      var image_Accu_precip_snow_LST = getAccu_precip_snow_LST(year, month, start, finish)
      var image_Snowmelt_temp_LST = getSnowmelt_temp_LST(year, month, start, finish)
      var image_Snowmelt_rad_LST = getSnowmelt_rad_LST(year, month, start, finish)
      var image_Snowmelt_rad_LST_LE_SH = getSnowmelt_rad_LST_LE_SH(year, month, start, finish)
      var image_Snowmelt_rad_temp_LE_HE = getSnowmelt_rad_temp_LE_HE(year, month, start, finish)
      



      var image_SH_era5 = getSH_ERA5(start, finish)
      
     
      var imgs = ee.List([
        image_getPrecip_MODIS,
        // image_getNDVI_MODIS,
        image_getEVI_MODIS,
        image_getLAI_MODIS,
        image_getLandCover_MODIS,
        image_getET_MODIS,
        image_getPET_MODIS,
        image_getSnowAlbedo_MODIS,
        image_getSnowCoverage_MODIS,
        image_getAlbedo_MODIS,
        image_getLST_MODIS,
        // image_getIncomingShortRad_GLDAS,
        image_Biome.select(["BIOME_NUM"]),
        image_Biome.select(["ECO_ID"]),
        image_Basin,
        image_burnID.select(["ObjectID"]),
        image_net_short_RD,
        image_net_long_RD,
        image_net_RD,
        image_snowmelt,
        image_net_RD_snow,
        image_temp_era5,
        yearSnow,
        image_LE,

        image_net_RD_snow_LST,
        image_Accu_precip_snow,
        image_Snowmelt_temp,
        image_Snowmelt_rad,
        
        image_Accu_precip_snow_LST,
        image_Snowmelt_temp_LST,
        image_Snowmelt_rad_LST,
        image_Snowmelt_rad_LST_LE_SH,
        image_SH_era5,
        image_Snowmelt_rad_temp_LE_HE
        
        
        
      ]);
      
      // print(imgs)
      var selectedVar = [
        "ObjectID",	
        "BIOME_NUM","HYBAS_ID",		"EVI","Lai", "Albedo_WSA_shortwave_MODIS","Snow_Albedo","ET_MODIS","PET_MODIS",	"LST_MODIS",	"temp_era5","Precip_MODIS",		"snowmelt",
          	"net_short_Rad","net_long_Rad","net_Rad","net_Rad_snow","net_Rad_snow_LST","LE_MODIS","first_snow","last_snow",'Accu_precip_snow','snowmelt_temp','snowmelt_rad',
          	'Accu_precip_snow_LST',
          	'snowmelt_temp_LST',
          	'snowmelt_rad_LST',
          	'snowmelt_rad_LST_LE_SH','SH_ERA5','snowmelt_rad_temp_LE_HE',
          	"lat","lon"
          	]
      
      
   
           
      var image = ee.ImageCollection.fromImages(imgs).toBands();
      var bandNames = image.bandNames();
      // print(bandNames)
      var newBandNames = bandNames.map(function(name) {
        name = ee.String(name);
        var names = name.split("_");getGeometry2
        var newName = names.slice(1).join("_");
        return newName;
      })
      image = image.select(bandNames, newBandNames);
      // image = image.addBands(ee.Image.pixelLonLat()).toDouble();
      image = image.set("year", year)
      image = image.set("month", month)
      var fileName = 'fireYear_' + fireYear + '_Year_' + year + '_Month_' + month ;
      extractSnowTempRainAlbedo(featureCol,image, fileName, folderName, selectedVar);
 
 
      // var palette = [
      //   '000096','0064ff', '00b4ff', '33db80', '9beb4a',
      //   'ffeb00', 'ffb300', 'ff6400', 'eb1e00', 'af0000'
      // ];
      // var precipitationVis = {min:0, max: 400, palette: palette};
      
      // Map.addLayer(image_Accu_precip_snow_LST, precipitationVis, 'Precipitation');

      
        // var bandName = 12*(year-2001)+month-6
        // bandName = 'b' + '6'
        // var img_incoming_shorRD = IncomingSR.select(bandName)
        // var img_incoming_longRD = IncomingLR.select(bandName);
        // Map.addLayer(img_incoming_longRD, precipitationVis, 'Precipitation');

        
    }
  }
}


//************************************************************* MAIN **********************************************************************************************************

                      
function main(folderName, featureCol,snowStartYear,snowEndYear,monthStart,monthEnd,fireYear){
 
var range = ee.Filter.and(ee.Filter.lte("lat", 90),
                          ee.Filter.gte("lat", 0)
                          )

featureCol = featureCol.map(getGeometry2)
var properties = ["ObjectID",'lat','lon'];
var image_burnID = featureCol.reduceToImage({
                    properties: properties,
                    reducer: ee.Reducer.first().forEach(properties)
                  }); 
image_burnID = image_burnID.toDouble()
featureCol = featureCol.filter(range)
// print(featureCol)

ExtractImgValue(image_burnID, featureCol, folderName,snowStartYear,snowEndYear,monthStart,monthEnd,fireYear);

}

var pointsCol =  table6
// var folderName = 'Burn_0909_100km'
var folderName = 'Unbn_0909_100km'

var fireYear=2005;
var snowStartYear = 2020
var snowEndYear = 2020
var monthStart = 1
var monthEnd = 1

main(folderName, pointsCol, snowStartYear,snowEndYear,monthStart,monthEnd,fireYear)









