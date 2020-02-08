import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, Dimensions } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card'
import logo from '../assets/favicon.png';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import {Picker} from 'native-base';
import { IconButton } from 'react-native-paper';

const {width, height} = Dimensions.get('window');

class Calendario extends Component {

    state = {
        categorie: "tutto"
    };

    render() {
        return (
            
            <View style={styles.screen}>
                
                <CustomHeader parent={this.props} />
                
                <View style={styles.contentbar}>
                    <View style={styles.leftcontainer}>
                        <IconButton icon="arrow-left" onPress={() => this.props.navigation.navigate('ListaAnnunci')} />
                    </View>
                    <Text style={styles.title}>
                        Calendario
                    </Text>
                    <View style={styles.rightcontainer}></View>
                </View>
            

                <ScrollView showsVerticalScrollIndicator={false}>
                    <View style={styles.screen}>

                        <Picker
                            style={styles.picker} itemStyle={styles.pickerItem}
                            selectedValue={this.state.categorie}
                            onValueChange={(itemValue) => this.setState({categorie: itemValue})}
                            >
                            <Picker.Item label="Tutti gli animali" value="tutto" />
                            <Picker.Item label="Cani" value="cani" />
                            <Picker.Item label="Gatti" value="gatti" />
                            <Picker.Item label="Conigli" value="conigli" />
                            <Picker.Item label="Volatili" value="volatili" />
                            <Picker.Item label="Rettili" value="rettili" />
                            <Picker.Item label="Altro" value="altro" />
                        </Picker>

                        <View style={{paddingBottom: 5}}></View>

                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('DettagliAnnuncio', {id_annuncio: '1'})}>
                            <Card style={styles.inputContainerGreen}>
                                <View style={styles.image}>
                                    <Image source={logo} style={styles.annuncioLogo}  />
                                </View>
                                

                                <View style={styles.data}>
                                    <Text style={styles.annuncioTitle} numberOfLines={1}>Cerco petsitter a colombaro di formigine c'erano tre alberi</Text>
                                    
                                    <Text style={styles.annuncioSubtitle} numberOfLines={2}>Bobi cerca un petsitter e sempre sarà dodò dell'albero azzurro e poi sai che non si sa</Text>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Data: </Text>
                                        <Text>12/11/2020 - 13/11/2020</Text>
                                    </View>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Pubblicato da: </Text>
                                        <Text>werther</Text>
                                    </View>
                                </View>
                            </Card>
                        </TouchableOpacity>

                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('DettagliAnnuncio', {id_annuncio: '1'})}>
                            <Card style={styles.inputContainerRed}>
                                <View style={styles.image}>
                                    <Image source={logo} style={styles.annuncioLogo}  />
                                </View>
                                

                                <View style={styles.data}>
                                    <Text style={styles.annuncioTitle} numberOfLines={1}>Cerco petsitter a colombaro di formigine c'erano tre alberi</Text>
                                    
                                    <Text style={styles.annuncioSubtitle} numberOfLines={2}>Bobi cerca un petsitter e sempre sarà dodò dell'albero azzurro e poi sai che non si sa</Text>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Data: </Text>
                                        <Text>12/11/2020 - 13/11/2020</Text>
                                    </View>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Pubblicato da: </Text>
                                        <Text>werther</Text>
                                    </View>
                                </View>
                            </Card>
                        </TouchableOpacity>
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
    annuncioLogo: {
        width: 80,
        height: 80
    },
    title: {
        fontSize: 20,
        marginVertical: 10
    },
    inputContainerGreen: {
        minWidth: '96%',
        flexDirection: 'row',
        alignItems: "center",
        borderColor: "green",
        borderWidth: 3
    },
    inputContainerRed: {
        minWidth: '96%',
        flexDirection: 'row',
        alignItems: "center",
        borderColor: "red",
        borderWidth: 3
    },
    annuncioTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        width: width - width / 2.6
    },
    annuncioSubtitle: {
        width: width - width / 2.6
    },
    data: {
        flex: 1
    },
    image: {
        paddingRight: 10
    },
    textInline: {
        flexDirection: 'row'
    },
    touchableopacity: {
        alignItems: 'center'
    },
    picker: {
        width: '90%',
        height: 40,
        backgroundColor: '#e7e7e7',
        borderColor: 'black',
        borderWidth: 3
    },
    pickerItem: {
        color: 'white'
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
    }
});

export default Calendario;