import React, { Component } from 'react';
import { View, Text, StyleSheet, Image, ScrollView, Button, ActivityIndicator, Dimensions } from 'react-native';
import CustomHeader from '../components/Header';
import { IconButton } from 'react-native-paper';
import logo from '../assets/pet_coin.png';
import Card from '../components/Card';


const {width, height} = Dimensions.get('window');

class Cassa extends Component {

    constructor(props){
        super(props);
        this.state ={ 
            isLoading: true
        }
    }
    
    componentDidMount() {
        this.fetchProfilo();
        
        this.willFocusSubscription = this.props.navigation.addListener(
          'willFocus',
          () => {
            this.setState({
                isLoading: true
            });
            this.fetchProfilo();
          }
        );
    }

    componentWillUnmount() {
    this.willFocusSubscription.remove();
    }

    fetchProfilo() {
        return fetch('http://2.224.160.133.xip.io/api/utenti/profilo/' + global.user_id + '/?format=json')
        .then((response) => response.json())
        .then((responseJson) => {
        
        this.setState({
            isLoading: false,
            dataSource: responseJson
        }, function(){

        });

        })
        .catch((error) =>{
        this.fetchProfilo();
        });
    }

    modificaSaldo(value) {
        fetch('http://2.224.160.133.xip.io/api/utenti/cassa/',
            {
              method: 'PUT',
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + global.user_key,
              },
              body: JSON.stringify({
                pet_coins: value,
              }),
            })
            .then(res => res.json())
            .then((res) => {
                this.fetchProfilo();
            })
            .then(obj =>  {
              callback(obj)
            })
            .catch((error) => {
                this.modificaSaldo;
            })
    }

    render() {

        if(this.state.isLoading){
            return(
                <View style={{flex: 1, paddingTop: height / 2}}>
                    <ActivityIndicator/>
                </View>
            )
        }

        data = this.state.dataSource;

        return (
            <View style={styles.screen}>
                <CustomHeader parent={this.props} />
                
                <View style={styles.contentbar}>
                    <View style={styles.leftcontainer}>
                        <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                    </View>
                    <Text style={styles.title}>
                        Acquista o vendi Pet Coins
                    </Text>
                    <View style={styles.rightcontainer}></View>
                </View>

                <ScrollView showsVerticalScrollIndicator={false}>
                    <View style={{alignItems: 'center'}}>
                        <Card style={styles.inputContainer}>
                        
                            <View style={{flexDirection: 'row', marginTop: 20}}>
                                <Text>Saldo attuale: </Text>
                                <Text>{data.pet_coins}</Text>
                                <Image source={logo} style={{ width: 25, height: 25 }}  />
                            </View>
                            
                            <View style={{marginTop: 20}}>
                                <Text style={styles.subtitle}>Acquista Pet Coins:</Text>
                            </View>
                            <View style={{flexDirection: 'row'}}>
                                <View style={styles.buttonStyle}>
                                    <Button title="+50" onPress={() => {
                                                this.modificaSaldo("50");}} />
                                </View>
                                <View style={styles.buttonStyle}>
                                    <Button title="+100" onPress={() => {
                                                this.modificaSaldo("100");}} />
                                </View>
                                <View style={styles.buttonStyle}>
                                    <Button title="+200" onPress={() => {
                                                this.modificaSaldo("200");}} />
                                </View>
                            </View>

                            <View style={{marginTop: 20}}>
                                <Text style={styles.subtitle}>Vendi Pet Coins:</Text>
                            </View>
                            <View style={{flexDirection: 'row'}}>
                                <View style={styles.buttonStyle}>
                                    <Button title="-50" onPress={() => {
                                                this.modificaSaldo("-50");}} />
                                </View>
                                <View style={styles.buttonStyle}>
                                    <Button title="-100" onPress={() => {
                                                this.modificaSaldo("-100");}} />
                                </View>
                                <View style={styles.buttonStyle}>
                                    <Button title="-200" onPress={() => {
                                                this.modificaSaldo("-200");}} />
                                </View>
                            </View>
                            
                        </Card>
                    </View>
                </ScrollView>
            </View>
        );
    }
}

const styles = StyleSheet.create({
    screen: {
        flex: 1
    },
    title: {
        fontSize: 20,
        marginVertical: 10
    },
    contentbar: {
        height: 50,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center'
      },
    leftcontainer: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'flex-start'
    },
    rightcontainer: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'flex-end',
        alignItems: 'center'
    },
    inputContainer: {
        minWidth: '96%'
    },
    subtitle: {
        fontSize: 18
    },
    buttonStyle: {
        padding: 10,
        width: 100
    }
});

export default Cassa;