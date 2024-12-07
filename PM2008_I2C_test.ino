#include <pm2008_i2c.h>

// #ifdef PM2008N

PM2008_I2C pm2008_i2c;

void setup() {
#ifdef PM2008N
  // wait for PM2008N to be changed to I2C mode
  delay(1000);
#endif
  pm2008_i2c.begin();
  Serial.begin(115200);
  pm2008_i2c.command();
  delay(1000);
}

void loop() {
  uint8_t ret = pm2008_i2c.read();
  if (ret == 0) {
  
    Serial.print("PM 2.5 (GRIMM) : : ");
    Serial.println(pm2008_i2c.pm2p5_grimm);

    Serial.print("PM 2.5 (TSI) : : ");
    Serial.println(pm2008_i2c.pm2p5_tsi);
   
  }
  delay(1000);
}
