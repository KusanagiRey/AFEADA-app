import 'package:flutter/material.dart';
import 'package:afeada/widget/aboutNews.dart';
import 'package:afeada/widget/backgroundimage.dart';
import 'package:afeada/widget/heartIcon.dart';

class StackWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Stack(
      alignment: Alignment.center,
      children: <Widget>[
        BackgroundImage(),
        AboutNew(),
        Positioned(
          right: 50,
          top: 150,
            child: HeartIcon())
      ],
    );
  }

}