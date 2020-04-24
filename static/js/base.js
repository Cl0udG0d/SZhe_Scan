var dom = document.getElementById("container");
var myChart = echarts.init(dom);
var app = {};

app.title = "环形图";

var option = {
  tooltip: {
    trigger: "item",
    formatter: "{a} <br/>{b}: {c} ({d}%)",
  },
  color: ["#93D8A9", "#FFB99D", "#AF7DCC", "#FFD83D", "#bbe2e8"],
  legend: {
    orient: "horizontal",
    x: "left",
    data: ["直接访问", "邮件营销", "联盟广告", "视频广告", "搜索引擎"],
  },
  series: [
    {
      name: "访问来源",
      type: "pie",
      radius: ["30%", "70%"],
      avoidLabelOverlap: false,
      label: {
        normal: {
          show: false,
          position: "center",
        },
        emphasis: {
          show: true,
          textStyle: {
            fontSize: "30",
            fontWeight: "bold",
          },
        },
      },
      labelLine: {
        normal: {
          show: false,
        },
      },
      data: [
        {
          value: 335,
          name: "直接访问",
        },
        {
          value: 310,
          name: "邮件营销",
        },
        {
          value: 234,
          name: "联盟广告",
        },
        {
          value: 135,
          name: "视频广告",
        },
        {
          value: 1548,
          name: "搜索引擎",
        },
      ],
    },
  ],
};
if (option && typeof option === "object") {
  myChart.setOption(option, true);
}
