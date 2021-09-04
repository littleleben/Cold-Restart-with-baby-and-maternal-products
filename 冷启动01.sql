CREATE TABLE tmp.tmp_zzp_UserColdStart_ordertable_count AS
SELECT 
	fbuyer_id fuid,
    orc_cate_code3,orc_cate_name3,--三级类目喜欢购买哪些？
    fdeal_source,--订单渠道
    count(*) buy_times,--购买次数
    round(avg(cast(fitem_origin_price as double)/100),2) buy_avgprice --价格信息
    --正常购买的价格区间是什么
FROM 
	adm.adm_sku_oms_orders_non_third_trade_dt_de 
WHERE 
	dt>='2021-07-01' and dt<='2021-07-31'--时间可修改
GROUP BY
	fbuyer_id,
    orc_cate_code3,
    orc_cate_name3,
    fdeal_source

--直接无法匹配dim表，所以先根据订单表中出现的用户进行提取
CREATE TABLE tmp.tmp_zzp_UserColdStart_fuid_feature AS 
SELECT 
	distinct fuid,--会员
	creator_city_code,creator_city_name,--注册城市
	register_source,--注册渠道
	sb_age,--BB年龄
	sb_sex--宝宝性别
		
FROM
    dim.dim_user_da      
WHERE
    dt='2021-08-01'
	AND fuid in (select fuid from tmp.tmp_zzp_UserColdStart_ordertable_count)



--①
--按照价格区间对人群进行划分
CREATE TABLE tmp.tmp_zzp_UserColdStart_ordertable_feature_buy_avgprice AS
SELECT 
	fuid,
    round(avg(buy_avgprice),2) buy_avgprice
FROM tmp.tmp_zzp_UserColdStart_ordertable_count 
GROUP BY fuid


--价格因素关联会员信息表
CREATE TABLE tmp.tmp_zzp_UserColdStart_ordertable_feature_buy_avgprice_data AS
SELECT
	T2.*,
	T1.buy_avgprice
   
FROM 
	tmp.tmp_zzp_UserColdStart_ordertable_feature_buy_avgprice T1
JOIN
	tmp.tmp_zzp_UserColdStart_fuid_feature T2
ON 
	T1.fuid=T2.fuid



--②
--按照经常购买的品类对人群进行划分
CREATE TABLE tmp.tmp_zzp_UserColdStart_ordertable_feature_buy_goodscate AS
SELECT 
	fuid,
	orc_cate_code3,
	orc_cate_name3,
    sum(buy_times) buy_times
FROM tmp.tmp_zzp_UserColdStart_ordertable_count 
group by 	fuid,
	orc_cate_code3,
	orc_cate_name3
	

--常购买的品类因素关联会员信息表--后面找出用户群体喜欢购买的20种品类（线上总3级品类是89种）
CREATE TABLE tmp.tmp_zzp_UserColdStart_ordertable_feature_buy_goodscate_data AS
SELECT
	T2.*,
	T1.orc_cate_code3,
	T1.orc_cate_name3,
    T1.buy_times
   
FROM 
	tmp.tmp_zzp_UserColdStart_ordertable_feature_buy_goodscate T1
JOIN
	tmp.tmp_zzp_UserColdStart_fuid_feature T2
ON 
	T1.fuid=T2.fuid

