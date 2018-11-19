
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `goods_choiceness`;
CREATE TABLE `goods_choiceness` (
               `id` int(11) NOT NULL AUTO_INCREMENT,
               `goods_id`    varchar(16) NOT  NULL comment '商品id',
               `goods_name`  varchar(128) DEFAULT NULL comment '商品名称',
               `goods_master_url`    varchar(1024) DEFAULT NULL comment '商品主图',
               `goods_detail_url`    varchar(1024) DEFAULT NULL comment '商品详情页链接地址',
               `goods_category`   varchar(32)  DEFAULT  NULL comment '商品一级类目',
               `goods_tbke_url`    varchar(1024) DEFAULT NULL comment '淘宝客链接',
               `goods_price`  varchar(8) DEFAULT NULL comment '商品价格',
               `goods_month_sales`  varchar(16)  DEFAULT  NULL comment '商品月销量',
               `income_rate`     varchar(8) DEFAULT NULL comment '收入比率',
               `seller_brokerage`    varchar(8) DEFAULT NULL comment '佣金',
               `seller_wangwang`  varchar(64) DEFAULT NULL comment '卖家旺旺',
               `seller_id`  varchar(16) DEFAULT NULL comment '卖家id',
               `shop_name`        varchar(128)  DEFAULT  NULL comment '店铺名称',
               `platform_type`    varchar(8) DEFAULT NULL comment '平台类型',
               `coupons_id`    varchar(32) DEFAULT NULL comment '优惠券id',
               `coupons_sum`   varchar(8) DEFAULT NULL comment '优惠券总量',
               `coupons_remain`  varchar(8) DEFAULT NULL comment '优惠券剩余量',
               `coupons_denomination`    varchar(128) DEFAULT NULL comment '优惠券面额',
               `coupons_begindate`  datetime DEFAULT NULL comment '优惠券开始时间',
               `coupons_enddate`  datetime DEFAULT NULL comment '优惠券结束时间',
               `coupons_url`  varchar(1024) DEFAULT NULL comment '优惠券链接',
               `coupons_promote_url`  varchar(1024) DEFAULT NULL comment '商品优惠券推广链接',
              PRIMARY KEY (`id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT  CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;


# 17
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `goods_groupbuying`;
CREATE TABLE `goods_groupbuying` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `goods_id` varchar(16)  DEFAULT  NULL comment '商品id',
              `goods_name` varchar(128)  DEFAULT  NULL comment '商品标题',
              `goods_price`    varchar(8) DEFAULT NULL comment '一人价（原价）',
              `group_purchase_price`    varchar(8) NOT  NULL comment '拼成价',
              `group_purchase_number`  varchar(8) DEFAULT NULL comment '几人团',
              `goods_url` varchar(1024) DEFAULT NULL comment '商品主图',
              `goods_begindate`  datetime DEFAULT NULL comment '开始时间',
              `goods_enddate`    datetime DEFAULT NULL comment '结束时间',
              `inventory_sum`     varchar(8) DEFAULT NULL comment '库存数量',
              `inventory_sold`       varchar(8) DEFAULT NULL comment '已售数量',
              `inventory_remain`    varchar(8) DEFAULT NULL comment '剩余库存',
              `promote_longurl`    varchar(1024) DEFAULT NULL comment '推广长链接',
              `promote_shorturl`    varchar(1024) DEFAULT NULL comment '推广短链接',
              `brokerage_rate`  varchar(8) DEFAULT NULL comment '佣金比率（%）',
              `brokerage_price`  varchar(8) DEFAULT NULL comment '佣金金额',
              `primary_categories_id`  varchar(64) DEFAULT NULL comment '一级类目id',
              `primary_categories_name`  varchar(64) DEFAULT NULL comment '一级类目名称 ',
              PRIMARY KEY (`id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;


# 16
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `goods_quality`;
CREATE TABLE `goods_quality` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `category_name` varchar(32)  DEFAULT  NULL comment '类目名称',
              `seller_nickname`   varchar(32)  DEFAULT  NULL comment '卖家昵称',
              `platform_type`    varchar(8) DEFAULT NULL comment '平台类型',
              `goods_id`    varchar(16) NOT  NULL comment '商品id',
              `goods_name`  varchar(128) DEFAULT NULL comment '商品名称',
              `goods_promote_url`    varchar(1024) DEFAULT NULL comment '商品推广链接',
              `goods_master_url`  varchar(1024) DEFAULT NULL comment '商品主图',
              `goods_price`    varchar(8) DEFAULT NULL comment '商品价格',
              `income_rate`     varchar(8) DEFAULT NULL comment '收入比率(%)',
              `coupons_denomination`  varchar(8) DEFAULT NULL comment '优惠券面额',
              `coupons_price`    varchar(8) DEFAULT NULL comment '券后价',
              `coupons_sum`    varchar(11) DEFAULT NULL comment '优惠券总量',
              `coupons_remain`   varchar(8) DEFAULT NULL comment '优惠券剩余量',
              `coupons_begindate`  datetime DEFAULT NULL comment '优惠券开始时间',
              `coupons_enddate`  datetime DEFAULT NULL comment '优惠券结束时间',
              `coupons_promote_url`    varchar(1024) DEFAULT NULL comment '优惠券推广链接',
              PRIMARY KEY (`id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;






