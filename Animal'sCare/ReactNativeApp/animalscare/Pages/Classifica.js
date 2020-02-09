import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image, Dimensions } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';
import {Picker} from 'native-base';
import profile_image from '../assets/profile_img.jpg';
import { IconButton } from 'react-native-paper';

const {width, height} = Dimensions.get('window');

class Classifica extends Component {

    state = {
        categorie: "generale",
        ordina: "voto"
    };

    render() {
        return (
            
            <View style={styles.screen}>
                
                <CustomHeader parent={this.props} />
                
                <View style={styles.contentbar}>
                    <View style={styles.leftcontainer}>
                        <IconButton icon="arrow-left" onPress={() => this.props.navigation.goBack(null)} />
                    </View>
                    <Text style={styles.title}>
                        Classifica
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
                            <Picker.Item label="Classifica generale" value="generale" />
                            <Picker.Item label="Classifica dei petsitter" value="petsitter" />
                            <Picker.Item label="Classifica degli utenti normali" value="pet" />
                        </Picker>

                        <View style={{paddingBottom: 5}}></View>

                        <Picker
                            style={styles.picker} itemStyle={styles.pickerItem}
                            selectedValue={this.state.ordina}
                            onValueChange={(itemValue) => this.setState({animali: itemValue})}
                            >
                            <Picker.Item label="Ordina per voto" value="voto" />
                            <Picker.Item label="Ordina per numero di recensioni ricevute" value="recensioni" />
                        </Picker>


                        <View style={{paddingBottom: 2}}></View>

                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('ProfiloNormale', {id_profilo: '1'})}>
                            <Card style={styles.inputContainer}>
                                <View style={styles.image}>
                                    <Image source={profile_image} style={styles.profileLogo}  />
                                </View>
                                

                                <View style={styles.data}>
                                    <Text style={styles.profileName} numberOfLines={1}>Werther Berselli</Text>
                                    
                                    <Text style={styles.profileData} numberOfLines={2}>Utente normale, Via Secchia 1/B, Formigine</Text>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto medio: </Text>
                                        <Text>5/5</Text>
                                    </View>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Recensioni ricevute: </Text>
                                        <Text>1</Text>
                                    </View>
                                </View>
                            </Card>
                        </TouchableOpacity>

                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('ProfiloNormale', {id_profilo: '1'})}>
                            <Card style={styles.inputContainer}>
                                <View style={styles.image}>
                                    <Image source={profile_image} style={styles.profileLogo}  />
                                </View>
                                

                                <View style={styles.data}>
                                    <Text style={styles.profileName} numberOfLines={1}>Werther Berselli</Text>
                                    
                                    <Text style={styles.profileData} numberOfLines={2}>Utente normale, Via Secchia 1/B, Formigine</Text>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto medio: </Text>
                                        <Text>5/5</Text>
                                    </View>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Recensioni ricevute: </Text>
                                        <Text>1</Text>
                                    </View>
                                </View>
                            </Card>
                        </TouchableOpacity>

                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('ProfiloNormale', {id_profilo: '1'})}>
                            <Card style={styles.inputContainer}>
                                <View style={styles.image}>
                                    <Image source={profile_image} style={styles.profileLogo}  />
                                </View>
                                

                                <View style={styles.data}>
                                    <Text style={styles.profileName} numberOfLines={1}>Werther Berselli</Text>
                                    
                                    <Text style={styles.profileData} numberOfLines={2}>Utente normale, Via Secchia 1/B, Formigine</Text>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto medio: </Text>
                                        <Text>5/5</Text>
                                    </View>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Recensioni ricevute: </Text>
                                        <Text>1</Text>
                                    </View>
                                </View>
                            </Card>
                        </TouchableOpacity>
                        
                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('ProfiloNormale', {id_profilo: '1'})}>
                            <Card style={styles.inputContainer}>
                                <View style={styles.image}>
                                    <Image source={profile_image} style={styles.profileLogo}  />
                                </View>
                                

                                <View style={styles.data}>
                                    <Text style={styles.profileName} numberOfLines={1}>Werther Berselli</Text>
                                    
                                    <Text style={styles.profileData} numberOfLines={2}>Utente normale, Via Secchia 1/B, Formigine</Text>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto medio: </Text>
                                        <Text>5/5</Text>
                                    </View>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Recensioni ricevute: </Text>
                                        <Text>1</Text>
                                    </View>
                                </View>
                            </Card>
                        </TouchableOpacity>

                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8} onPress={() => this.props.navigation.navigate('ProfiloNormale', {id_profilo: '1'})}>
                            <Card style={styles.inputContainer}>
                                <View style={styles.image}>
                                    <Image source={profile_image} style={styles.profileLogo}  />
                                </View>
                                

                                <View style={styles.data}>
                                    <Text style={styles.profileName} numberOfLines={1}>Werther Berselli</Text>
                                    
                                    <Text style={styles.profileData} numberOfLines={2}>Utente normale, Via Secchia 1/B, Formigine</Text>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Voto medio: </Text>
                                        <Text>5/5</Text>
                                    </View>
                                    <View style={styles.textInline}>
                                        <Text style={{fontWeight: 'bold', fontStyle: 'italic'}}>Recensioni ricevute: </Text>
                                        <Text>1</Text>
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
    profileLogo: {
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
    profileName: {
        fontSize: 18,
        fontWeight: 'bold',
        width: width - width / 2.6
    },
    profileData: {
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

export default Classifica;