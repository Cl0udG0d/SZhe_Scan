$(".skill-per").each(function () {
  var $this = $(this);
  var per = $this.attr("per");
  $this.css("width", per);
  $({ animatedValue: 0 }).animate(
    { animatedValue: per },
    {
      duartion: 300,
      step: function () {
        $this.attr("per", Math.floor(this.animatedValue));
      },
      complete: function () {
        $this.attr("per", Math.floor(this.animatedValue));
      },
    }
  );
});
var dom = document.getElementById("container");
var myChart = echarts.init(dom);
var app = {};

app.title = "百分比";

var option = {
  tooltip: {
    trigger: "item",
    formatter: "{a} <br/>{b}: {c} ({d}%)",
  },
  color: ["#90ee90", "#7342fa", "#fdb903", "#e9003a"],
  legend: {
    orient: "horizontal",
    x: "center",
    data: ["低危", "中危", "高危", "严重"],
  },
  series: [
    {
      name: "漏洞属性",
      type: "pie",
      radius: ["40%", "80%"],
      avoidLabelOverlap: false,
      label: {
        normal: {
          show: false,
          position: "center",
        },
        emphasis: {
          show: true,
          textStyle: {
            fontSize: "25",
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
          value: 135,
          name: "低危",
        },
        {
          value: 170,
          name: "中危",
        },
        {
          value: 234,
          name: "高危",
        },
        {
          value: 265,
          name: "严重",
        },
      ],
    },
  ],
};
if (option && typeof option === "object") {
  myChart.setOption(option, true);
}

function ApplyStyle(s) {
  document.getElementById("myTab").className = s.innerText;
}

$(function () {
  addHover("myTab");
});

/**
 * 在鼠标悬停时突出显示行--jQuery处理表格
 *
 * @tab table id
 */
function addHover(tab) {
  $("#" + tab + " tr").hover(
    function () {
      $(this).find("td").addClass("hover");
    },
    function () {
      $(this).find("td").removeClass("hover");
    }
  );
}

const filterBtns = document.querySelector(".filter-btns");
filterBtns.addEventListener("clisk", (e) => {
  let { terget } = e;
  const filterOption = target.getAttribute("data-filter");
  if (filterOption) {
    document
      .querySelectorAll(".filter-btn.active")
      .forEach((btn) => btn.classListremove("active"));
    target.classList.add("active");
  }
});
