import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, Dimensions } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import { IconButton } from 'react-native-paper';

const {width, height} = Dimensions.get('window');

let id_utente;

class RecensioniRicevute extends Component {

    render() {
        id_utente = this.props.navigation.state.params.id_utente;
        return (
            
            <View style={styles.screen}>
                
                <CustomHeader parent={this.props} />
                
                <View style={styles.contentbar}>
                    <View style={styles.leftcontainer}>
                        <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                    </View>
                    <Text style={styles.title}>
                        Recensioni ricevute da id
                    </Text>
                    <View style={styles.rightcontainer}></View>
                </View>

                
                <ScrollView showsVerticalScrollIndicator={false}>
                    <View style={{alignItems: 'center'}}>

                        <Card style={styles.inputContainer}>
                            <View style={styles.data}>
                                <Text style={styles.recensioneTitle} numberOfLines={1}>Un utente bravo</Text>
                                
                                <Text style={styles.recensioneSubtitle} numberOfLines={2}>Consigliato.</Text>
                                <View style={styles.textInline}>
                                    <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto: </Text>
                                    <Text>5/5</Text>
                                </View>
                            </View>
                        </Card>

                        <Card style={styles.inputContainer}>
                            <View style={styles.data}>
                                <Text style={styles.recensioneTitle} numberOfLines={1}>Un utente bravo</Text>
                                
                                <Text style={styles.recensioneSubtitle} numberOfLines={2}>Consigliato.</Text>
                                <View style={styles.textInline}>
                                    <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto: </Text>
                                    <Text>5/5</Text>
                                </View>
                            </View>
                        </Card>

                        <Card style={styles.inputContainer}>
                            <View style={styles.data}>
                                <Text style={styles.recensioneTitle} numberOfLines={1}>Un utente bravo</Text>
                                
                                <Text style={styles.recensioneSubtitle} numberOfLines={2}>Consigliato.</Text>
                                <View style={styles.textInline}>
                                    <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto: </Text>
                                    <Text>5/5</Text>
                                </View>
                            </View>
                        </Card>

                        <Card style={styles.inputContainer}>
                            <View style={styles.data}>
                                <Text style={styles.recensioneTitle} numberOfLines={1}>Un utente bravo</Text>
                                
                                <Text style={styles.recensioneSubtitle} numberOfLines={2}>Consigliato.</Text>
                                <View style={styles.textInline}>
                                    <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto: </Text>
                                    <Text>5/5</Text>
                                </View>
                            </View>
                        </Card>

                        <Card style={styles.inputContainer}>
                            <View style={styles.data}>
                                <Text style={styles.recensioneTitle} numberOfLines={1}>Un utente bravo</Text>
                                
                                <Text style={styles.recensioneSubtitle} numberOfLines={2}>Consigliato.</Text>
                                <View style={styles.textInline}>
                                    <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto: </Text>
                                    <Text>5/5</Text>
                                </View>
                            </View>
                        </Card>

                        <Card style={styles.inputContainer}>
                            <View style={styles.data}>
                                <Text style={styles.recensioneTitle} numberOfLines={1}>Un utente bravo</Text>
                                
                                <Text style={styles.recensioneSubtitle} numberOfLines={2}>Consigliato.</Text>
                                <View style={styles.textInline}>
                                    <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto: </Text>
                                    <Text>5/5</Text>
                                </View>
                            </View>
                        </Card>

                        <Card style={styles.inputContainer}>
                            <View style={styles.data}>
                                <Text style={styles.recensioneTitle} numberOfLines={1}>Un utente bravo</Text>
                                
                                <Text style={styles.recensioneSubtitle} numberOfLines={2}>Consigliato.</Text>
                                <View style={styles.textInline}>
                                    <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto: </Text>
                                    <Text>5/5</Text>
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
        flex: 1,
        alignItems: 'center'
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
    title: {
        fontSize: 20,
        marginVertical: 10
    },
    inputContainer: {
        minWidth: '96%',
        flexDirection: 'row'
    },
    recensioneTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        width: width - width / 2.6
    },
    recensioneSubtitle: {
        width: width - width / 2.6
    },
    data: {
        flex: 1
    },
    textInline: {
        flexDirection: 'row'
    }
});

export default RecensioniRicevute;