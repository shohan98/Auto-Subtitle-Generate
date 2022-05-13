import boto3
import json
from django.conf import settings


class Subtitle:
    def __init__(self, JsonFileLocation):
        self.JsonFileLocation = JsonFileLocation
        
    
    def getTimeCode(self, seconds ):
        # Format and return a string that contains the converted number of seconds into subtitle format
        t_hund = int(seconds % 1 * 1000)
        tseconds = int( seconds )
        tsecs = ((float( tseconds) / 60) % 1) * 60
        tmins = int( tseconds / 60 )
        return str( "%02d:%02d:%02d,%03d" % (00, tmins, int(tsecs), t_hund))
    
    
        
    def GetWordsFromJson(self):
        File = open(self.JsonFileLocation, 'r', encoding="utf-8")
        ReadJson = File.read()
        LoadJson = json.loads(ReadJson)
        result = LoadJson['results']['speaker_labels']['segments']
        word = LoadJson['results']['items']
        
        speaker_label = []
        create_line = []
        new_line = []
        punc = 0
        end_time = 0
        for ii in result:
            for j in ii['items']:
                
                speaker_label.append(j['speaker_label'])
        for i in word:
            if i['type']!='punctuation':
                WordDetails = {}
                WordDetails['start_time'] = i['start_time']
                WordDetails['end_time'] = i['end_time']
                WordDetails['word'] = i['alternatives'][0]['content']
                create_line.append(WordDetails)
                if float(WordDetails['start_time'])-float(end_time)>=2.00:
                    punc=0
                    new_line.append(end_time)
                end_time = i['end_time']
            else:
                punc+=1
                create_line[-1]['word'] = create_line[-1]['word']+i['alternatives'][0]['content']
                
                if punc==2:
                    punc = 0
                    new_line.append(end_time)
                elif i['alternatives'][0]['content']!=',':
                    # create_line[-1]['word'] = create_line[-1]['word']+'<br>'
                    create_line[-1]['word'] = create_line[-1]['word']
                
        l = len(speaker_label)
        global new_result
        new_result = []
        
        for i in range(l):
            value = {}
            value['s_t'] = create_line[i]['start_time']
            value['e_t'] = create_line[i]['end_time']
            value['word'] = create_line[i]['word']
            value['speaker'] = speaker_label[i]
            new_result.append(value)
            
    
        phrase =  {}
        phrase['words'] = []
        phrases = []
        nPhrase = True
        i = 0
        speaker = ''
        for item in new_result:
            if nPhrase == True:
                speaker = item['speaker']
                phrase = {}
                phrase["start_time"] = self.getTimeCode( float(item["s_t"]) )
                phrase['words'] = []
                
                nPhrase = False
            
            
    
            if item['e_t'] in new_line:
                phrase['words'].append(item['word'])
                i+=1
                phrase["end_time"] = self.getTimeCode( float(item["e_t"]) )
                phrases.append(phrase)
                nPhrase = True
            elif speaker!=item['speaker']:
                speaker = item['speaker']
                phrase["end_time"] = self.getTimeCode( float(item["e_t"]) )
                phrases.append(phrase)
                speaker = item['speaker']
                phrase = {}
                phrase["start_time"] = self.getTimeCode( float(item["s_t"]) )
                phrase['words'] = [item['word']]
                
            else:
                phrase['words'].append(item['word'])
            
        return phrases
    
    
    
    def subtitle(self, filename, extension='srt', SaveSubtitleLocation=''):
        
            
        # try:
        JsonFile = self.GetWordsFromJson()
        print(SaveSubtitleLocation)
        srt_file = SaveSubtitleLocation+'{}.{}'.format(filename, extension)
    
        srt = open(srt_file,'w')
        for i in range(len(JsonFile)):
            srt.write(str(i+1)+'\n')
            srt.write(str(JsonFile[i]['start_time'])+' --> '+ str(JsonFile[i]['end_time'])+'\n')
            srt_value = ' '.join(JsonFile[i]['words'])+'\n\n'     
            
            
            srt.write(srt_value.replace('\n ','\n'))
        srt.close()
        
        return {'message':"Subtitle write complete", 'srt_file':srt_file, 'status': 1}
        # except Exception as e:
        #     return {'message':str(e), 'srt_file':'', 'status': 0}
    
    def GenerateSubtitleWithTranslate(self, filename, sourceLangCode, targetLangCode, 
                region_name=settings.AWS_REGION, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                aws_secret_access_key=settings.AWS_ACCESS_KEY, extension='srt'):
        try:
            translate = boto3.client(
                'translate',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name = region_name
            )
        
            
        except:
            return {'status':401, 'sub_file':''}
        try:
            JsonFile = self.GetWordsFromJson()
            t_sub_file = '{}'.format(filename)+sourceLangCode+'-'+targetLangCode+'.'+extension
            t_sub = open(t_sub_file,'w')
            if extension=='vtt':
                t_sub.write('WEBVTT\n\n')
            sub_file = '{}.srt'.format(filename)
            sub = open(sub_file,'w')
            
            
            for i in range(len(JsonFile)):
                sub.write(str(i+1)+'\n')
                sub.write(str(JsonFile[i]['start_time']).replace(',','.')+' --> '+ str(JsonFile[i]['end_time']).replace(',','.')+'\n')
                sub_value = ' '.join(JsonFile[i]['words'])+'\n\n'     
                
                if sourceLangCode!=targetLangCode:
                    t_sub.write('\n'+str(i+1)+'\n')
                    t_sub.write(str(JsonFile[i]['start_time']).replace(',','.')+' --> '+ str(JsonFile[i]['end_time']).replace(',','.')+'\n')
                    t_sub_value = translate.translate_text(Text=sub_value.replace('<br>',''),SourceLanguageCode=sourceLangCode, TargetLanguageCode=targetLangCode)
                    if '<br>' in sub_value:    
                        t_sub.write(t_sub_value['TranslatedText']+'<br>'+'\n\n')
                    else:
                        t_sub.write(t_sub_value['TranslatedText']+'\n\n')
                
                sub.write(sub_value.replace('\n ','\n'))
            sub.close()
            
            if sourceLangCode!=targetLangCode:
                t_sub.close()
                
            return {'status':"Subtitle write complete", 'sub_file':sub_file, 'translate_sub_file':t_sub_file}
        except:
            return {'status':'Subtitle write Failed', 'sub_file':'', 'translate_sub_file':''}
       
       
       
       
       
       