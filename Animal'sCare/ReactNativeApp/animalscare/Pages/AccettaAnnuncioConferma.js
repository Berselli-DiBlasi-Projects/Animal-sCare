import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, ActivityIndicator } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import { Dimensions } from 'react-native';

const {width, height} = Dimensions.get('window');

let title;

class AccettaAnnuncioConferma extends Component {

    constructor(props){
        super(props);
        this.state ={
            annuncio_user: ""
        }
    }

    componentDidMount() {
        this.fetchDettagliAnnuncio();
        this.willFocusSubscription = this.props.navigation.addListener(
          'willFocus',
          () => {
            this.setState({
                isLoading: true,
            }, function(){
    
            });
            this.fetchDettagliAnnuncio();
          }
        );
    }

    componentWillUnmount() {
        this.willFocusSubscription.remove();
    }

    fetchDettagliAnnuncio() {
        return fetch('http://2.224.160.133.xip.io/api/annunci/' + this.props.navigation.state.params.id_annuncio + '/dettagli/?format=json')
        .then((response) => response.json())
        .then((responseJson) => {
        this.setState({
            isLoading: false,
            annuncio_user: responseJson.annuncio.user.username
        }, function(){

        });

        })
        .catch((error) =>{
        this.fetchDettagliAnnuncio();
        });
    }
    
    accettaAnnuncio() {
        console.log("ciao");
        fetch('http://2.224.160.133.xip.io/api/annunci/' + this.props.navigation.state.params.id_annuncio + '/accetta/',
            {
              method: 'PUT',
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + global.user_key,
              },
              body: JSON.stringify({
                annuncio: {
                    user_accetta: true
                }
              }),
            })
            .then(res => res.json())
            .then((res) => {
                console.log(JSON.stringify(res));
                this.props.navigation.navigate('ListaAnnunci');
            })
            .then(obj =>  {
              callback(obj)
            })
            .catch((error) => {
                console.log("err");
                this.accettaAnnuncio;
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

        title = "Accetti l'annuncio di ";
        title += this.state.annuncio_user;
        title += "?";

        return (
                
            <View style={styles.screen}>
                <CustomHeader parent={this.props} />
                

                <View style={{alignItems: 'center'}}>
                    <Card style={styles.inputContainer}>
                        <View style={{flexDirection: 'row'}}>
                            <Text style={styles.title}>{title}</Text>
                        </View>

                        <View style={styles.controlli}>
                            <View style={styles.buttonview}>
                                <Button title="Indietro" onPress={() => this.props.navigation.goBack(null)}/>
                            </View>
                            <View style={styles.buttonview}>
                                <Button title="Conferma" onPress={() => {
                                            this.accettaAnnuncio();}} />
                            </View>
                        </View>
                    </Card>
                </View>
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
    buttonview: {
        width: 110,
        paddingRight: 5,
        paddingLeft: 5
    },
    inputContainer: {
        minWidth: '96%'
    },
    controlli: {
        flexDirection: 'row',
        paddingTop: 20
    }
});

export default AccettaAnnuncioConferma;