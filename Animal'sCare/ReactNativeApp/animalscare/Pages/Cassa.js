import React, { Component } from 'react';
import { View, Text, StyleSheet, Image, ScrollView, Button } from 'react-native';
import CustomHeader from '../components/Header';
import { IconButton } from 'react-native-paper';
import logo from '../assets/pet_coin.png';
import Card from '../components/Card';

class Cassa extends Component {

    render() {
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
                                <Text>2550</Text>
                                <Image source={logo} style={{ width: 25, height: 25 }}  />
                            </View>
                            
                            <View style={{marginTop: 20}}>
                                <Text style={styles.subtitle}>Acquista Pet Coins:</Text>
                            </View>
                            <View style={{flexDirection: 'row'}}>
                                <View style={styles.buttonStyle}>
                                    <Button title="+50" />
                                </View>
                                <View style={styles.buttonStyle}>
                                    <Button title="+100" />
                                </View>
                                <View style={styles.buttonStyle}>
                                    <Button title="+200" />
                                </View>
                            </View>

                            <View style={{marginTop: 20}}>
                                <Text style={styles.subtitle}>Vendi Pet Coins:</Text>
                            </View>
                            <View style={{flexDirection: 'row'}}>
                                <View style={styles.buttonStyle}>
                                    <Button title="-50" />
                                </View>
                                <View style={styles.buttonStyle}>
                                    <Button title="-100" />
                                </View>
                                <View style={styles.buttonStyle}>
                                    <Button title="-200" />
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