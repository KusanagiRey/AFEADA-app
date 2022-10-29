import 'package:flutter/material.dart';
import 'package:salomon_bottom_bar/salomon_bottom_bar.dart';
import 'package:afeada/news_preference.dart';
import 'package:afeada/widget/profile_widget.dart';
import 'package:afeada/pages/stack.dart';


class News extends StatefulWidget {
  const News({Key? key}): super(key: key);

  @override
  NewsScreen createState() => NewsScreen();
}

class NewsScreen extends State<News> {

  void _onTapped (int index)
  {
    switch(index)
    {
      case 0:
        break;
      case 1:
        Navigator.pushNamedAndRemoveUntil(context, "/calendar", (route) => false);
        break;
      case 2:
        Navigator.pushNamedAndRemoveUntil(context, "/profile", (route) => false);
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AFEADA',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Scaffold(
        appBar: AppBar(
          title: const Padding(padding: EdgeInsets.only(left: 15), child: Text("Новости"),),
          backgroundColor: const Color(0xff252850),
          titleTextStyle: const TextStyle(
              color: Color(0xffE6E6FA),
              fontSize: 24.0,
              fontStyle: FontStyle.normal
          ),
          actions: [
            IconButton(
              icon: const Icon(Icons.draw_outlined, size: 30.0),
              onPressed: (){

              },
              color: const Color(0xffE6E6FA),
              padding: const EdgeInsets.only(
                  right: 20
              ),
            )
          ],
        ),
        body: Container(
          //color: const Color(0xff1E1E1E),
           child: ListView.builder(
             itemCount: 20,
             prototypeItem: ListTile(
               title: Text("Новость"),
             ),
             itemBuilder: (context, index) {
               return ListTile(
                 title: Text("Новость $index"),
               );
             },
           ),
           ),
        bottomNavigationBar: Container (
          color: const Color(0xff252850),
          child: SalomonBottomBar(
            items: [
              SalomonBottomBarItem(icon: const Icon(Icons.thumb_up), title: const Text("Новости"), selectedColor: const Color(0xffE6E6FA)),
              SalomonBottomBarItem(icon: const Icon(Icons.calendar_month), title: const Text("Календарь"), selectedColor: const Color(0xffE6E6FA)),
              SalomonBottomBarItem(icon: const Icon(Icons.person), title: const Text("Профиль"), selectedColor: const Color(0xffE6E6FA)),
            ],
            margin: const EdgeInsets.only(
              left: 20,
              right: 20,
              top: 5,
              bottom: 5,
            ),
            currentIndex: 0,
            selectedItemColor: const Color(0xffE6E6FA),
            unselectedItemColor: const Color(0xffE6E6FA),
            onTap: _onTapped,
          ),
        )
      ),
    );
  }
}
