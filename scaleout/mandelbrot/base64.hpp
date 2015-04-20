const char *base64encode( char *p )
{
    static const char b64_charset[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

    std::string ret;
    unsigned char block_3[3];
    unsigned char block_4[4];
    char *str;
    int i = 0,
        j = 0,
        size;

    size = strlen(str);

    while( size-- ){
        block_3[i++] = *(str++);
        if( i == 3 ){
            block_4[0] = (block_3[0] & 0xfc) >> 2;
            block_4[1] = ((block_3[0] & 0x03) << 4) + ((block_3[1] & 0xf0) >> 4);
            block_4[2] = ((block_3[1] & 0x0f) << 2) + ((block_3[2] & 0xc0) >> 6);
            block_4[3] = block_3[2] & 0x3f;

            for(i = 0; (i <4) ; i++){
                ret += b64_charset[block_4[i]];
            }
            i = 0;
        }
    }

    if(i){
        for(j = i; j < 3; j++){
            block_3[j] = '\0';
        }
        block_4[0] = (block_3[0] & 0xfc) >> 2;
        block_4[1] = ((block_3[0] & 0x03) << 4) + ((block_3[1] & 0xf0) >> 4);
        block_4[2] = ((block_3[1] & 0x0f) << 2) + ((block_3[2] & 0xc0) >> 6);
        block_4[3] = block_3[2] & 0x3f;

        for(j = 0; (j < i + 1); j++){
            ret += b64_charset[block_4[j]];
        }
        while((i++ < 3)){
            ret += '=';
        }
    }

    return ret.c_str();
}

const char *base64decode( char *p ){
    static const std::string b64_charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    std::string ret;
    char * str;
    int in_len,
        i = 0,
        j = 0,
        in_ = 0;
    unsigned char block_4[4], block_3[3];

    in_len = strlen(str);

    while( in_len-- && ( str[in_] != '=') && is_base64(str[in_]) ){
        block_4[i++] = str[in_];
        in_++;
        if( i == 4 ){
            for( i = 0; i < 4; i++ ){
                block_4[i] = b64_charset.find(block_4[i]);
            }
            block_3[0] = (block_4[0] << 2) + ((block_4[1] & 0x30) >> 4);
            block_3[1] = ((block_4[1] & 0xf) << 4) + ((block_4[2] & 0x3c) >> 2);
            block_3[2] = ((block_4[2] & 0x3) << 6) + block_4[3];

            for( i = 0; (i < 3); i++ ){
                ret += block_3[i];
            }
            i = 0;
        }
    }

    if(i){
        for( j = i; j <4; j++ ){
            block_4[j] = 0;
        }

        for( j = 0; j < 4; j++ ){
            block_4[j] = b64_charset.find(block_4[j]);
        }

        block_3[0] = (block_4[0] << 2) + ((block_4[1] & 0x30) >> 4);
        block_3[1] = ((block_4[1] & 0xf) << 4) + ((block_4[2] & 0x3c) >> 2);
        block_3[2] = ((block_4[2] & 0x3) << 6) + block_4[3];

        for( j = 0; (j < i - 1); j++ ){
            ret += block_3[j];
        }
    }

    return ret.c_str();
}
