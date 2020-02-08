import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, Dimensions } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card'
import logo from '../assets/favicon.png';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import {Picker} from 'native-base';

const {width, height} = Dimensions.get('window');

class ListaAnnunci extends Component {

    state = {
        categorie: "tutto",
        animali: "tutto",
        ordina: "non_ordinare"
    };

    render() {
        return (
            
            <View style={styles.screen}>
                
                <CustomHeader parent={this.props} />
                
                <Text style={styles.title}>Annunci</Text>
                
            

                <ScrollView showsVerticalScrollIndicator={false}>
                    <View style={styles.screen}>

                        <Picker
                            style={styles.picker} itemStyle={styles.pickerItem}
                            selectedValue={this.state.categorie}
                            onValueChange={(itemValue) => this.setState({categorie: itemValue})}
                            >
                            <Picker.Item label="Tutte le categorie di annunci" value="tutto" />
                            <Picker.Item label="Cerco un petsitter" value="petsitter" />
                            <Picker.Item label="Cerco un pet" value="pet" />
                        </Picker>

                        <View style={{paddingBottom: 5}}></View>

                        <Picker
                            style={styles.picker} itemStyle={styles.pickerItem}
                            selectedValue={this.state.animali}
                            onValueChange={(itemValue) => this.setState({animali: itemValue})}
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

                        <Picker
                            style={styles.picker} itemStyle={styles.pickerItem}
                            selectedValue={this.state.ordina}
                            onValueChange={(itemValue) => this.setState({ordina: itemValue})}
                            >
                            <Picker.Item label="Non ordinare gli annunci" value="non_ordinare" />
                            <Picker.Item label="Distanza geografica crescente" value="crescente" />
                            <Picker.Item label="Distanza geografica decrescente" value="decrescente" />
                        </Picker>

                        <View style={{paddingBottom: 2}}></View>

                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('DettagliAnnuncio', {id_annuncio: '1'})}>
                            <Card style={styles.inputContainer}>
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

                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('DettagliAnnuncio', {id_annuncio: '2'})}>
                            <Card style={styles.inputContainer}>
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
                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('DettagliAnnuncio', {id_annuncio: '3'})}>
                            <Card style={styles.inputContainer}>
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
                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('DettagliAnnuncio', {id_annuncio: '4'})}>
                            <Card style={styles.inputContainer}>
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
                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('DettagliAnnuncio', {id_annuncio: '5'})}>
                            <Card style={styles.inputContainer}>
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
                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('DettagliAnnuncio', {id_annuncio: '6'})}>
                            <Card style={styles.inputContainer}>
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
    inputContainer: {
        minWidth: '96%',
        flexDirection: 'row'
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
    }
});

export default ListaAnnunci;