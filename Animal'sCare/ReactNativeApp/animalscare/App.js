import React, { Component } from 'react';
import { Text, View, SafeAreaView, ScrollView, Dimensions, Image } from 'react-native';
import { createAppContainer } from 'react-navigation';
import {createStackNavigator} from 'react-navigation-stack';
import { createDrawerNavigator, DrawerItems } from 'react-navigation-drawer';
import ListaAnnunci from './Pages/ListaAnnunci';
import InserisciAnnuncio from './Pages/InserisciAnnuncio';
import Classifica from './Pages/Classifica';
import CercaUtente from './Pages/CercaUtente';
import Profilo from './Pages/Profilo';
import Calendario from './Pages/Calendario';
import Cassa from './Pages/Cassa';
import Contattaci from './Pages/Contattaci';
import Login from './Pages/Login';
import DettagliAnnuncio from './Pages/DettagliAnnuncio';
import AccettaAnnuncioConferma from './Pages/AccettaAnnuncioConferma';
import EliminaAnnuncioConferma from './Pages/EliminaAnnuncioConferma';
import * as Font from 'expo-font';
import logo from './assets/favicon.png';

const {width, height} = Dimensions.get('window');

const CustomDrawerNavigation = (props) => {
  return (
  <SafeAreaView style={{ flex: 1 }}>
    <View style={{ height: 250, backgroundColor: '#d2d2d2', opacity: 0.9 }}>
      <View style={{ height: 200, backgroundColor: 'Green', alignItems: 'center', justifyContent: 'center' }}>
        <Image source={require('./assets/no-image.png')} style={{ height: 150, width: 150, borderRadius: 60 }} />
      </View>
      <View style={{ height: 50, backgroundColor: 'Green', alignItems: 'center', justifyContent: 'center' }}>
        <Text>John Doe</Text>
      </View>
    </View>
    <ScrollView>
      <DrawerItems {...props}/>
    </ScrollView>
    <View style={{ alignItems: "center", backgroundColor: '#c4c4c4' }}>
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
      title: 'Annunci'
    }
  },
  InserisciAnnuncio: {
    screen: InserisciAnnuncio,
    navigationOptions: {
      title: 'Inserisci annuncio'
    }
  },
  Classifica: {
    screen: Classifica,
    navigationOptions: {
      title: 'Classifica'
    }
  },
  CercaUtente: {
    screen: CercaUtente,
    navigationOptions: {
      title: 'Cerca utente'
    }
  },
  Profilo: {
    screen: Profilo,
    navigationOptions: {
      title: 'Profilo'
    }
  },
  Calendario: {
    screen: Calendario,
    navigationOptions: {
      title: 'Calendario'
    }
  },
  Cassa: {
    screen: Cassa,
    navigationOptions: {
      title: 'Cassa'
    }
  },
  Contattaci: {
    screen: Contattaci,
    navigationOptions: {
      title: 'Contattaci'
    }
  },
  Login: {
    screen: Login,
    navigationOptions: {
      title: 'Login'
    }
  },
  DettagliAnnuncio: {
    screen: DettagliAnnuncio,
    navigationOptions: {
      title: 'Dettagli annuncio'
    }
  },
  AccettaAnnuncioConferma: {
    screen: AccettaAnnuncioConferma,
    navigationOptions: {
      title: 'Accetta annuncio conferma'
    }
  },
  EliminaAnnuncioConferma: {
    screen: EliminaAnnuncioConferma,
    navigationOptions: {
      title: 'Elimina annuncio conferma'
    }
  }
},
{
  drawerPosition: 'left',
  contentComponent: CustomDrawerNavigation,
  drawerOpenRoute: 'DrawerOpen',
  drawerCloseRoute: 'DrawerClose',
  drawerToggleRoute: 'DrawerToggle',
  drawerWidth: (width / 3) * 2
});

const AppContainer = createAppContainer(Drawer)

export default class App extends React.Component {
  
  state = {
    fontLoaded: false,
  };

  async componentDidMount() {
    await Font.loadAsync({
      'satisfy': require('./assets/fonts/satisfy.ttf'),
      'typold-medium': require('./assets/fonts/typold-medium.otf')
    });

    this.setState({ fontLoaded: true });
  }

  render () {
    if (!this.state.fontLoaded) {
      return (
        <View></View>
      );
    }

    return (
      <AppContainer />
    );
  }
}
