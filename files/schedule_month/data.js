﻿$axure.loadCurrentPage({
  "url":"schedule_month.html",
  "generationDate":new Date(1413916421323.88),
  "isCanvasEnabled":false,
  "variables":["OnLoadVariable"],
  "page":{
    "packageId":"c04c19b8cee94d4ea9fc3c2026fc8a73",
    "type":"Axure:Page",
    "name":"Schedule_month",
    "notes":{
      "Instructions":"<p><span>Month Screen</span></p><p><span>&nbsp; &nbsp;&nbsp; - Month calendar</span></p><p><span>&nbsp; &nbsp;&nbsp; - By clicking a specific day the user can scroll through the specific schedules on this day and edit them</span></p><p><span>&nbsp; &nbsp; &nbsp;&nbsp; (Not currently shown in this screen)</span></p><p><span>&nbsp; &nbsp;&nbsp; - By clicking back you return to the home screen</span></p>"},
    "style":{
      "baseStyle":"627587b6038d43cca051c114ac41ad32",
      "pageAlignment":"near",
      "fill":{
        "fillType":"solid",
        "color":0xFFFFFFFF},
      "image":null,
      "imageHorizontalAlignment":"near",
      "imageVerticalAlignment":"near",
      "imageRepeat":"auto",
      "favicon":null,
      "sketchFactor":"0",
      "colorStyle":"appliedColor",
      "fontName":"Applied Font",
      "borderWidth":"0"},
    "adaptiveStyles":{
},
    "interactionMap":{
},
    "diagram":{
      "objects":[{
          "id":"9074f5113b0e476b97981f773e4a60ec",
          "label":"",
          "type":"imageBox",
          "styleType":"imageBox",
          "visible":true,
          "style":{
            "size":{
              "width":360,
              "height":640}},
          "adaptiveStyles":{
},
          "objects":[{
              "id":"4c7de01681174eb4a97370feeb673915",
              "label":"",
              "isContained":true,
              "type":"richTextPanel",
              "styleType":"paragraph",
              "visible":true,
              "style":{
                "size":{
                  "width":360,
                  "height":640}},
              "adaptiveStyles":{
}}],
          "images":{
            "normal~":"images/schedule_month/u0.png"}},
{
          "id":"d065add718bd4a62906d7872dd27fb79",
          "label":"Day",
          "type":"dynamicPanel",
          "styleType":"dynamicPanel",
          "visible":true,
          "style":{
            "location":{
              "x":23,
              "y":67},
            "size":{
              "width":90,
              "height":40}},
          "adaptiveStyles":{
},
          "interactionMap":{
            "onClick":{
              "description":"OnClick",
              "cases":[{
                  "description":"Case 1",
                  "isNewIfGroup":false,
                  "actions":[{
                      "action":"linkWindow",
                      "description":"Open Schedule in Current Window",
                      "target":{
                        "targetType":"page",
                        "url":"schedule.html",
                        "includeVariables":true},
                      "linkType":"current"}]}]}},
          "tabbable":true,
          "scrollbars":"none",
          "fitToContent":false,
          "propagate":false,
          "diagrams":[{
              "id":"34edcf6b910b4018b2b19ec020144cf8",
              "label":"State1",
              "type":"Axure:PanelDiagram",
              "objects":[],
              "style":{
                "fill":{
                  "fillType":"solid",
                  "color":0xFFFFFF},
                "image":null,
                "imageHorizontalAlignment":"near",
                "imageVerticalAlignment":"near",
                "imageRepeat":"auto"},
              "adaptiveStyles":{
}}]},
{
          "id":"d171ee81fbf349c495557a175fba5ac1",
          "label":"Back",
          "type":"dynamicPanel",
          "styleType":"dynamicPanel",
          "visible":true,
          "style":{
            "size":{
              "width":40,
              "height":60}},
          "adaptiveStyles":{
},
          "interactionMap":{
            "onClick":{
              "description":"OnClick",
              "cases":[{
                  "description":"Case 1",
                  "isNewIfGroup":false,
                  "actions":[{
                      "action":"linkWindow",
                      "description":"Open Main in Current Window",
                      "target":{
                        "targetType":"page",
                        "url":"main.html",
                        "includeVariables":true},
                      "linkType":"current"}]}]}},
          "tabbable":true,
          "scrollbars":"none",
          "fitToContent":false,
          "propagate":false,
          "diagrams":[{
              "id":"a6baeafda8df47a29df3d586360686e8",
              "label":"State1",
              "type":"Axure:PanelDiagram",
              "objects":[],
              "style":{
                "fill":{
                  "fillType":"solid",
                  "color":0xFFFFFF},
                "image":null,
                "imageHorizontalAlignment":"near",
                "imageVerticalAlignment":"near",
                "imageRepeat":"auto"},
              "adaptiveStyles":{
}}]}]}},
  "masters":{
},
  "objectPaths":{
    "9074f5113b0e476b97981f773e4a60ec":{
      "scriptId":"u0"},
    "4c7de01681174eb4a97370feeb673915":{
      "scriptId":"u1"},
    "d065add718bd4a62906d7872dd27fb79":{
      "scriptId":"u2"},
    "d171ee81fbf349c495557a175fba5ac1":{
      "scriptId":"u3"}}});