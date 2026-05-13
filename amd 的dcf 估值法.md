我这里**不用 $10.253B 作为 Data Center 基数**，因为它是 AMD **公司总营收**。分部 DCF 应该拆成：

- Data Center：Q1 2026 revenue **$5.775B**，年化 **$23.10B**
    
- Client + Gaming：Q1 revenue **$3.605B**，年化 **$14.42B**
    
- Embedded：Q1 revenue **$0.873B**，年化 **$3.492B**
    

AMD 官方 Q1 2026 总营收是 **$10.253B**；Data Center、Client/Gaming、Embedded 分别为 **$5.775B / $3.605B / $0.873B**。([Advanced Micro Devices, Inc.](https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results "AMD Reports First Quarter 2026 Financial Results :: Advanced Micro Devices, Inc. (AMD)"))  
当前 AMD 市值我按约 **$740B** 对比，finance 工具显示约 **$739.7B**。

## 计算口径

公式：

[  
PV=\sum_{t=1}^{10}\frac{Revenue_t \times NetMargin_t}{(1+9%)^t}  
]

假设：

- Data Center：Year 1 revenue = $5.775B × 4 = **$23.10B**
    
- Data Center 净利率：从 **17%** 线性上升到 **35% / 40% / 45%**
    
- Data Center revenue CAGR：**30% / 40% / 50%**
    
- Client + Gaming：Year 1 revenue = **$14.42B**，净利率 **16%**，年增长 **10%**
    
- Embedded：Year 1 revenue = **$3.492B**，用当前 segment operating income / revenue 作为净利率近似：$338M / $873M ≈ **38.7%**，年增长 **5%**
    
- 不考虑 capex、营运资本、终值；10 年后价值归 0
    

## 固定部分现值

|分部|10 年现金流现值|
|---|--:|
|Client + Gaming|**$22.1B**|
|Embedded|**$10.5B**|
|固定部分合计|**$32.6B**|

## Data Center 敏感度：AMD 股权价值估算

单位：**十亿美元**

|Data Center 年增长|DC 净利率到 35%|DC 净利率到 40%|DC 净利率到 45%|
|--:|--:|--:|--:|
|**30%**|**$185.2B**|**$202.6B**|**$219.9B**|
|**40%**|**$281.3B**|**$310.9B**|**$340.5B**|
|**50%**|**$434.5B**|**$484.0B**|**$533.5B**|

这里的数值已经包含 Client + Gaming 和 Embedded。

## 和当前市值对比

按当前市值约 **$740B**：

|场景|估值|相对当前市值|
|---|--:|--:|
|30% 增长、40% 终局净利率|**$202.6B**|约 **-73%**|
|40% 增长、40% 终局净利率|**$310.9B**|约 **-58%**|
|50% 增长、40% 终局净利率|**$484.0B**|约 **-35%**|
|50% 增长、45% 终局净利率|**$533.5B**|约 **-28%**|

## 结论

按你这个“**10 年现金流、无终值、无 capex、无残值**”的口径，AMD 的估值核心区间大约是：

**$200B–$534B**

中性一点的假设，也就是 **Data Center 年增长 30%、净利率从 17% 提升到 40%**，算出来只有：

**约 $203B**

即使给到很激进的 **Data Center 年增长 50%、净利率提升到 45%**，也只有：

**约 $534B**

所以在这个模型下，AMD 当前约 **$740B** 市值已经隐含了更强的条件，例如：

1. Data Center 高增长持续超过 10 年；
    
2. 10 年后仍然有很高终值，而不是归 0；
    
3. AI GPU / CPU 的净利率比 45% 更高；
    
4. Client、Gaming、Embedded 也有更高利润弹性；
    
5. 市场在给 AMD “成为第二个 Nvidia 生态位”的期权价值。
    

另外，你提到的 **$10.253B** 是 AMD 全公司季度总营收，不是 Data Center 营收。如果把 $10.253B 误当成 Data Center 的季度收入再额外加 Client/Gaming/Embedded，会重复计算。