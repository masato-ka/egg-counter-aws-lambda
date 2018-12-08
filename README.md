# Egg Counter AWS Lambda function.


## Overview 

This is a Egg Counter AWS Lambda Function.
See in [detail](http://masato-ka.hatenablog.com/entry/2018/12/08/112034) 


## Usage

Please deploy your AWS Lambda by Cloud Formation with template.yml.
And You should specify parameter below the table.

| Parameter name| Description  |
|:--------------|:-------------|
|DeviceIdParameter|Device id that got from [SORACOM Inventory](https://soracom.jp/services/inventory/).|
|DeviceSecretParameter|Device secret that got from [SORACOM Inventory](https://soracom.jp/services/inventory/).|
|AuthKeyParameter|AuthKey that got from SORACOM User. User type is should be [SAM users](https://blog.soracom.jp/blog/2016/01/27/soracom-access-management/).|
|MaxRemainingParameter| Initial quantities of your same stock. When reset counter, latest quantities is replased this number.|


## Version
      
* 2018/12/08  Version 1.0.0
     

## Author

 * Name : masato-ka
 * E-mai: jp6uzv at gmail.com
 * Twitter: @masato_ka

## LICENCE

MIT License
