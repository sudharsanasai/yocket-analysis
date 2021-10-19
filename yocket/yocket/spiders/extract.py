import scrapy
import pickle as pkl

'''
TODO:
1. Add Application Deadline

'''

class ShopcluesSpider(scrapy.Spider):
   #name of spider
    name = 'yocket'
    course_link_file = open('yocket/course_yocket_links.pkl','rb')
    start_urls = pkl.load(course_link_file)



    def parse(self, response):
       #Extract product information
        scraped_info = {}
        url = response.url
        url = url.replace('https://www.yocket.com/universities/','')
        scraped_info['university_name'] = url.split('/')[0]
        scraped_info['course_name'] = url.split('/')[1]
        
        details_response = response.xpath('//div[@id="Details"]/div/div/div/p/text()').extract()
        details_response = [stat.strip() for stat in details_response]

        # print(details_response)
        for stat in ['Annual Tuition Fee*','Course Duration', 'Course Credits',  'Delivery Medium']:
            if stat in details_response:
                stat_index = details_response.index(stat)

                stat_value = details_response[stat_index-1]
                stat_header = details_response[stat_index]
                scraped_info[stat_header] = stat_value.strip()
        if 'Course Link' in details_response:
            scraped_info['Course Link'] = response.xpath('//div[@id="Details"]/div/div/div/p/a')[0].attrib['href']
        if 'Tuition Link' in details_response:
            scraped_info['Tuition Link'] = response.xpath('//div[@id="Details"]/div/div/div/p/a')[-1].attrib['href']

        admission_response = response.xpath('//div[@id="Admissions"]/div/div/div/p/text()').extract()
        admission_response = [stat.strip() for stat in admission_response]
        if 'Application Fee' in admission_response:
            stat_index = admission_response.index('Application Fee')
            stat_value = admission_response[stat_index-1]
            stat_header = admission_response[stat_index]
            scraped_info[stat_header] = stat_value
        if 'Application Link' in admission_response:
            scraped_info['Application Link'] = response.xpath('//div[@id="Admissions"]/div/div/div/p/a')[-1].attrib['href']

        students_application_response = response.xpath('//div[@id="Students"]/div/div/p/text()').extract()
        students_application_response = [stat.strip() for stat in students_application_response]
        for stat in ['Yocketers have applied', 'Yocketers got admits', 'Yocketers are interested']:
            if stat in students_application_response:
                stat_index = students_application_response.index(stat)
                stat_value = students_application_response[stat_index-1]
                stat_header = students_application_response[stat_index]
                scraped_info[stat_header] = stat_value

        students_scores_response = response.xpath('//div[@id="Students"]/div/div/div/p/text()').extract()
        exams = ['GRE', 'TOEFL', 'IELTS']
        for i, score in enumerate(students_scores_response):
            print(students_scores_response)
            scraped_info[exams[i]] = score


        yield scraped_info