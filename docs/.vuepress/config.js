
module.exports = {
    title: '碎遮-风起',
	base: '/szhe-docs/',
    head: [ // 注入到当前页面的 HTML <head> 中的标签
      ['link', { rel: 'icon', href: '/logo.jpg' }], // 增加一个自定义的 favicon(网页标签的图标)
    ],
    themeConfig: {
      logo: '/logo.jpg',  // 左上角logo
      nav:[ // 导航栏配置
        {text: '首页', link: '/' },
        {text: '快速开始', link: '/quickStart/' },
		{text: '指南', link: '/guide/'},
        {text: '团队', link: '/team/'}  ,    
        {text: '常见问题', link: '/question/'},      
        {text: 'Github', link: 'https://github.com/Cl0udG0d/SZhe_Scan'}     
      ],
      sidebar: 'auto', // 侧边栏配置
    }
  };