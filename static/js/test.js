var ctx = document.getElementById("myChart").getContext("2d");
var data = {
  /// 表现在X轴上的数据，数组形式
  labels: ["January", "February", "March", "April", "May", "June", "July"],
  /// 第一条线
  datasets: [
    {
      /// 曲线的填充颜色
      fillColor: " rgb(86, 86, 240)",
      /// 填充块的边框线的颜色
      strokeColor: " rgb(86, 86, 240)",
      /// 表示数据的圆圈的颜色
      pointColor: " rgb(86, 86, 240)",
      /// 表示数据的圆圈的边的颜色
      pointStrokeColor: "#fff",
      data: [65.5, 59.2, 90, 81, 56, 55, 40],
    },
    /// 第二条线
    {
      // fillColor: "rgba(151,187,205,0.5)",
      // strokeColor: "rgba(151,187,205,1)",
      // pointColor: "rgba(151,187,205,1)",
      // pointStrokeColor: "#fff",
      // data: [28, 48, 40, 19, 96, 27, 100]

      /// 曲线的填充颜色
      fillColor: "#d3d3d3",
      /// 填充块的边框线的颜色
      strokeColor: "rgba(220,220,220,1)",
      /// 表示数据的圆圈的颜色
      pointColor: "rgba(220,220,220,1)",
      /// 表示数据的圆圈的边的颜色
      pointStrokeColor: "#fff",
      data: [27, 48, 40, 19, 96, 27, 10],
    },
  ],
};
/// 动画效果call
var options = {
  scaleFontStyle: "normal",
};
/// 创建对象，生成折线图表
// new Chart(ctx).Line(data, options);
//生成柱状图
new Chart(ctx).Bar(data);
