import 'package:afeada/model/user.dart';
import 'package:afeada/user_preferences.dart';
import 'package:flutter/material.dart';
import 'package:salomon_bottom_bar/salomon_bottom_bar.dart';
import 'package:afeada/widget/profile_widget.dart';
import 'package:afeada/widget/button_widget.dart';

class Profile extends StatefulWidget {
  const Profile({Key? key}): super(key: key);

  @override
  ProfileScreen createState() => ProfileScreen();
}

class ProfileScreen extends State<Profile> {
  void _onTapped (int index)
  {
    switch(index)
    {
      case 0:
        Navigator.pushNamedAndRemoveUntil(context, "/", (route) => false);
        break;
      case 1:
        Navigator.pushNamedAndRemoveUntil(context, "/calendar", (route) => false);
        break;
      case 2:
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    const user = UserPreferense.myUser;
    return MaterialApp(
      title: 'AFEADA',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Scaffold(
          appBar: AppBar(
            title: const Padding(padding: EdgeInsets.only(left: 15), child: Text("Профиль"),),
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
            //color: Color(0xff1E1E1E),
            child: ListView(
              physics: BouncingScrollPhysics(),
              children: [
                const SizedBox(height: 24),
                ProfileWidget(
                  imagePath: user.imagePath,
                  onClicked: () async {},
                ),
                const SizedBox(height: 24),
                buildName(user),
                const SizedBox(height: 24),
                Container(
                  height: 108,
                  margin: const EdgeInsets.only(
                    left: 20,
                    right: 20
                  ),
                  child: buildUpgradeButton1(),
                ),
                const SizedBox(height: 10),
                Container(
                  height: 78,
                  margin: const EdgeInsets.only(
                      left: 20,
                      right: 20
                  ),
                  child: buildUpgradeButton2(),
                ),
                const SizedBox(height: 15),
                Container(
                  margin: EdgeInsets.only(
                    left: 125,
                  ),
                  child: const Text('Характеристики', style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 20
                  ))
                ),
                const SizedBox(height: 15),
                Align(
                  alignment: Alignment.bottomLeft,
                  child: Container(
                    child: buildState(user),
                  ),
                ),
              ],
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
              currentIndex: 2,
              selectedItemColor: const Color(0xffE6E6FA),
              unselectedItemColor: const Color(0xffE6E6FA),
              onTap: _onTapped,
            ),
          )
      ),
    );
  }

  Widget buildName(User user) => Column(
    children: [
      Text(
        user.name,
        style: TextStyle(
          fontWeight: FontWeight.bold,
          fontSize: 24
        ),
      ),
      const SizedBox(height: 4)
    ],
  );

  Widget buildUpgradeButton1() => ButtonWidget(
    text: "Колода",
    onClicked: () {

    }
  );

  Widget buildUpgradeButton2() => ButtonWidget(
      text: "QR-код",
      onClicked: () {

      }
  );

  Widget buildState(User user) => Column(
    children: [
      Container(
          //margin: EdgeInsets.only(right: 40),
        child: Text(
          "Сила: " + user.Strength,
          style: TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 15,
          ),
        )
      ),
      Container(
        margin: EdgeInsets.only(left: 40),
        child: Text(
          "Ловкость: " + user.Agility,
          style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 15
          ),
          textAlign: TextAlign.left,
        ),
      ),
      Container(
        margin: EdgeInsets.only(left: 40),
        child: Text(
          "Гибкость: " + user.Flexibility,
          style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 15
          ),
        ),
      ),
      Container(
        margin: EdgeInsets.only(left: 80),
        child: Text(
          "Выносливость: " + user.Stamina,
          style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 15
          ),
        ),
      ),
      Container(
        margin: EdgeInsets.only(left: 130),
        child: Text(
          "Стрессоустойчивость: " + user.Stress_resist,
          style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 15
          ),
        ),
      )
    ],
  );
}