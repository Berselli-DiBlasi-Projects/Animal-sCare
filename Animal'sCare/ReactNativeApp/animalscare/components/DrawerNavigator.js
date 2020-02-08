import React, { Component } from 'react';
import { Text, View, SafeAreaView, ScrollView, Image } from 'react-native';
import { createDrawerNavigator, DrawerItems } from 'react-navigation-drawer';
import { Icon } from 'native-base';
import { Dimensions } from 'react-native';
import ListaAnnunci from '../Pages/ListaAnnunci';
import InserisciAnnuncio from '../Pages/InserisciAnnuncio';
import Classifica from '../Pages/Classifica';
import CercaUtente from '../Pages/CercaUtente';
import ProfiloNormale from '../Pages/ProfiloNormale';
import ProfiloPetsitter from '../Pages/ProfiloPetsitter';
import Calendario from '../Pages/Calendario';
import Cassa from '../Pages/Cassa';
import Contattaci from '../Pages/Contattaci';
import Login from '../Pages/Login';
import logo from '../assets/favicon.png';
import CustomStackNavigator from './StackNavigator';

const {width, height} = Dimensions.get('window');

const hiddenDrawerItems = ['CustomStackNavigator'];

const CustomDrawerNavigation = (props) => {
    
    return (
    <SafeAreaView style={{ flex: 1 }}>
      <View style={{ height: 250, backgroundColor: '#cfe3f3', opacity: 0.9 }}>
        <View style={{ height: 200, backgroundColor: 'Green', alignItems: 'center', justifyContent: 'center' }}>
          <Image source={require('../assets/no-image.png')} style={{ height: 150, width: 150, borderRadius: 60 }} />
        </View>
        <View style={{ height: 50, backgroundColor: 'Green', alignItems: 'center', justifyContent: 'center' }}>
          <Text>Utente non registrato</Text>
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
        navigationOptions: {
        title: 'Inserisci annuncio',
        drawerIcon: ({ tintColor }) => (
            <Icon name = "md-add" />
          )
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
    ProfiloNormale: {
        screen: ProfiloNormale,
        navigationOptions: {
        title: 'Profilo normale',
        drawerIcon: ({ tintColor }) => (
            <Icon name = "md-person" />
          )
        }
    },
    ProfiloPetsitter: {
      screen: ProfiloPetsitter,
      navigationOptions: {
      title: 'Profilo petsitter',
      drawerIcon: ({ tintColor }) => (
          <Icon name = "md-person" />
        )
      }
  },
    Calendario: {
        screen: Calendario,
        navigationOptions: {
        title: 'Calendario',
        drawerIcon: ({ tintColor }) => (
            <Icon name = "calendar" />
          )
        }
    },
    Cassa: {
        screen: Cassa,
        navigationOptions: {
        title: 'Cassa',
        drawerIcon: ({ tintColor }) => (
            <Icon name = "md-cart" />
          )
        }
    },
    Contattaci: {
        screen: Contattaci,
        navigationOptions: {
        title: 'Contattaci',
        drawerIcon: ({ tintColor }) => (
            <Icon name = "md-mail" />
          )
        }
    },
    Login: {
        screen: Login,
        navigationOptions: {
        title: 'Login',
        drawerIcon: ({ tintColor }) => (
            <Icon name = "md-power" />
          )
        }
    },
    CustomStackNavigator: {
        screen: CustomStackNavigator,
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