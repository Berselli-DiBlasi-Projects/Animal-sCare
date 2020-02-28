import React, { Component } from 'react';
import { Text, View, SafeAreaView, ScrollView, Image, Button } from 'react-native';
import { createDrawerNavigator, DrawerItems } from 'react-navigation-drawer';
import { Icon } from 'native-base';
import { Dimensions } from 'react-native';
import ListaAnnunci from '../Pages/ListaAnnunci';
import InserisciAnnuncio from '../Pages/InserisciAnnuncio';
import Classifica from '../Pages/Classifica';
import CercaUtente from '../Pages/CercaUtente';
import Calendario from '../Pages/Calendario';
import Cassa from '../Pages/Cassa';
import Contattaci from '../Pages/Contattaci';
import Login from '../Pages/Login';
import Logout from '../Pages/Logout';
import logo from '../assets/favicon.png';
import RegistrazioneStackNavigator from './RegistrazioneStackNavigator';
import AnnuncioStackNavigator from './AnnuncioStackNavigator';
import ProfiloStackNavigator from './ProfiloStackNavigator';

const {width, height} = Dimensions.get('window');

const hiddenDrawerItems = ['NestedDrawerNavigator'];

const CustomDrawerNavigation = (props) => {
    
    var label_utente = "";
    if (!global.logged_in) {
      label_utente = "Utente anonimo";
    } else {
      label_utente = global.username;
    }

    return (
    <SafeAreaView style={{ flex: 1 }}>
      <View style={{ height: 250, backgroundColor: '#cfe3f3', opacity: 0.9 }}>
        <View style={{ height: 200, backgroundColor: 'Green', alignItems: 'center', justifyContent: 'center' }}>
          <Image source={require('../assets/no-image.png')} style={{ height: 150, width: 150, borderRadius: 60 }} />
        </View>
        <View style={{ height: 50, backgroundColor: 'Green', alignItems: 'center', justifyContent: 'center' }}>
        <Text>{label_utente}</Text>
        </View>
      </View>
      <ScrollView>
        <DrawerItems {...props}/>
      </ScrollView>
      <View style={{ alignItems: "center", backgroundColor: '#e7e7e7' }}>
        <View style={{ flexDirection: 'row' }}>
          <Image source={logo} style={{ width: 25, height: 25 }}  />
          <Text style={{paddingTop: 2, fontFamily: 'typold-medium', color: '#7e7777'}}> BERSELLI, DI BLASI</Text>
          <Text style={{paddingTop: 3, color: '#7e7777'}}> - 2020</Text>
        </View>
      </View>
    </SafeAreaView>
    );
  }

const Drawer = createDrawerNavigator({
    ListaAnnunci: {
        screen: ListaAnnunci,
        navigationOptions: {
        title: 'Annunci',
        drawerIcon: ({ tintColor }) => (
            <Icon name = "md-clipboard" />
          )
        }
        
    },
    InserisciAnnuncio: {
        screen: InserisciAnnuncio,
        navigationOptions: ({navigation}) => {
          if(!global.logged_in) {
            return {
              drawerLabel: () => null
            }
          } else {
            return {
              title: 'Inserisci annuncio',
              drawerIcon: ({ tintColor }) => (
                <Icon name = "md-add" />
              )
            }
          }
        }
    },
    Classifica: {
        screen: Classifica,
        navigationOptions: {
        title: 'Classifica',
        drawerIcon: ({ tintColor }) => (
            <Icon name = "ios-star-outline" />
          )
        }
    },
    CercaUtente: {
        screen: CercaUtente,
        navigationOptions: {
        title: 'Cerca utente',
        drawerIcon: ({ tintColor }) => (
            <Icon name = "md-search" />
          )
        }
    },
    ProfiloStackNavigator: {
      screen: ProfiloStackNavigator,
      navigationOptions: ({navigation}) => {
        if(!global.logged_in) {
          return {
            drawerLabel: () => null
          }
        } else {
          return {
            title: 'Profilo',
            drawerIcon: ({ tintColor }) => (
              <Icon name = "md-person" />
            )
          }
        }
      }
    },
    Calendario: {
        screen: Calendario,
        navigationOptions: ({navigation}) => {
          if(!global.logged_in) {
            return {
              drawerLabel: () => null
            }
          } else {
            return {
              title: 'Calendario',
              drawerIcon: ({ tintColor }) => (
                <Icon name = "calendar" />
              )
            }
          }
        }
    },
    Cassa: {
        screen: Cassa,
        navigationOptions: ({navigation}) => {
          if(!global.logged_in) {
            return {
              drawerLabel: () => null
            }
          } else {
            return {
              title: 'Cassa',
              drawerIcon: ({ tintColor }) => (
                <Icon name = "md-cart" />
              )
            }
          }
        }
    },
    Contattaci: {
        screen: Contattaci,
        navigationOptions: ({navigation}) => {
          if(!global.logged_in) {
            return {
              drawerLabel: () => null
            }
          } else {
            return {
              title: 'Contattaci',
              drawerIcon: ({ tintColor }) => (
                <Icon name = "md-mail" />
              )
            }
          }
        }
    },
    RegistrazioneStackNavigator: {
      screen: RegistrazioneStackNavigator,
        navigationOptions: ({navigation}) => {
          if(global.logged_in) {
            return {
              drawerLabel: () => null
            }
          } else {
            return {
              title: 'Registrazione',
              drawerIcon: ({ tintColor }) => (
                <Icon name = "md-person-add" />
              )
            }
          }
        }
    },
    Login: {
        screen: Login,
        navigationOptions: ({navigation}) => {
          if(global.logged_in) {
            return {
              drawerLabel: () => null
            }
          } else {
            return {
              title: 'Login',
              drawerIcon: ({ tintColor }) => (
                <Icon name = "md-power" />
              )
            }
          }
        }
    },
    Logout: {
      screen: Logout,
      navigationOptions: ({navigation}) => {
        if(!global.logged_in) {
          return {
            drawerLabel: () => null
          }
        } else {
          return {
            title: 'Logout',
            drawerIcon: ({ tintColor }) => (
              <Icon name = "md-power" />
            )
          }
        }
      }
  },
    AnnuncioStackNavigator: {
      screen: AnnuncioStackNavigator,
      navigationOptions: ({navigation}) => {
            return {
              drawerLabel: () => null,
          }
      }
    }
},
{
    drawerPosition: 'left',
    contentComponent: CustomDrawerNavigation,
    drawerOpenRoute: 'DrawerOpen',
    drawerCloseRoute: 'DrawerClose',
    drawerToggleRoute: 'DrawerToggle',
    drawerWidth: (width / 3) * 2,
});

export default Drawer;