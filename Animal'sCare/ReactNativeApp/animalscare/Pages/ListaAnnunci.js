import React, { Component } from 'react';
import { View, Text, StyleSheet, Button, Image } from 'react-native';
import CustomHeader from '../components/Header';
import Card from '../components/Card'
import logo from '../assets/favicon.png';
import { TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native-gesture-handler';

class ListaAnnunci extends Component {

    render() {
        return (
            
            <View style={styles.screen}>
                
                <CustomHeader parent={this.props} />
                
                <Text style={styles.title}>Annunci</Text>
                
            

                <ScrollView showsVerticalScrollIndicator={false}>
                    <View style={styles.screen}>   
                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8}>
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

                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8}>
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
                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8}>
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
                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8}>
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
                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8}>
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
                        <TouchableOpacity style={styles.touchableopacity} activeOpacity={.8}>
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
        width: 220
    },
    annuncioSubtitle: {
        width: 220
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
    }
});

export default ListaAnnunci;