"""
Created on 2012-09-05

@author: skardan
"""
from skgaze.EMDAT.Participant import Participant
#def explore_validation_threshold_segments(datadir, prune_length = None, user_list = xrange(7,38),
#                  auto_partition_low_quality_segments = False):
#    
#    participants = []
#    pid = 55
#    seglen = 0
#    segs = 0
#    for rec in user_list:
#        print "pid:", pid
#        if rec<10:
#            allfile = datadir+'/Rec 0'+str(rec)+'-All-Data.tsv'
#            fixfile = datadir+'/Rec 0'+str(rec)+'-Fixation-Data.tsv'
#            evefile = datadir+'/Rec 0'+str(rec)+'-Event-Data.tsv'
#        else:
#            allfile = datadir+'/Rec '+str(rec)+'-All-Data.tsv'
#            fixfile = datadir+'/Rec '+str(rec)+'-Fixation-Data.tsv'
#            evefile = datadir+'/Rec '+str(rec)+'-Event-Data.tsv'
#        print allfile
#        import os.path
#        if os.path.exists(allfile):
#            p = Participant(pid, evefile, allfile, fixfile, aoifiles=None, prune_length = prune_length,
#                                require_valid_segs = False,
#                                auto_partition_low_quality_segments = auto_partition_low_quality_segments)
#            tvalidity = []
#            
#            for seg in p.segments:
#                seglen += seg.completion_time
#            segs += len(p.segments)
#
##            for tresh in range(1,100,1):##proportion
##                invc = 0
##                invsegs=[]
##                for seg in segments:
##                    if seg.calc_validity1(tresh/100.0) == False:
##                        invc +=1
##            for tresh in range(1,21,1):##prop-gap
##                invc = 0
##                invsegs=[]
##                for seg in segments:
##                    if seg.calc_validity2(tresh*seg.completion_time/100.0) == False:
##                        invc +=1                        
##            for tresh in range(1,20000,100):##time-gap
##                invc = 0
##                invsegs=[]
##                for seg in segments:
##                    if seg.calc_validity2(tresh) == False:
##                        invc +=1
#
#            for tresh in range(1,102,1):##proportion Fixation
#                invc = 0
#                invsegs=[]
#                for seg in p.segments:
#                    if seg.calc_validity3(tresh/100.0) == False:
#                        invc +=1                        
#                        invsegs.append(seg.segid)
#                        
#                if len(invsegs)>0:
#                    print "seg:",invsegs 
#                        
#                tvalidity.append((tresh, invc))
#            participants.append( (pid,tvalidity, len(p.segments) ) )
#            print ( (tvalidity, len(p.segments)) )
#           
#        pid += 1
#        print "average seg len",seglen/float(segs)
#    return participants

def explore_validation_proportion_threshold_segments(participant_list, include_restored_samples = True, prune_length = None, 
                                          auto_partition_low_quality_segments = False):
    """Explores different threshiold values for the proportion of valid samples method in terms of Segments for all Participants in the list
    """
    
    seglen = 0
    segs = 0
    participants = []
    for p in participant_list:
        print("pid:", p.pid)
        if p.require_valid_segments == True:
            raise Exception("explore_validation_threshold_segments should be called with a list of Participants with require_valid_segments = False")
            
        
        tvalidity = []
        
        for seg in p.segments:
            seglen += seg.completion_time
        segs += len(p.segments)
        if include_restored_samples == False:
            for tresh in range(1,102,1):    ##proportion
                invc = 0
                invsegs=[]
                for seg in p.segments:
                    if seg.calc_validity1(tresh/100.0) == False:
                        invc +=1

        else:
            for tresh in range(1,102,1):    ##proportion with restored samples from Fixations
                invc = 0
                invsegs=[]
                for seg in p.segments:
                    if seg.calc_validity3(tresh/100.0) == False:
                        invc +=1                        
                        invsegs.append(seg.segid)
                        
                if len(invsegs)>0:
                    print("seg:",invsegs)
                        
                tvalidity.append((tresh, invc))
        participants.append( (p.pid,tvalidity, len(p.segments) ) )
        print ( (tvalidity, len(p.segments)) )
       
    print("average seg len",seglen/float(segs))
    return participants

def explore_validation_time_gap_threshold_segments(participant_list, time_gap_list = [100, 200, 300, 400, 500, 1000, 2000], prune_length = None, 
                                          auto_partition_low_quality_segments = False):
    """Explores different threshiold values for the invalid time gaps in the Segments for all Participants in the list
    """
    
    seglen = 0
    segs = 0
    participants = []
    for p in participant_list:
        print("pid:", p.pid)
        if p.require_valid_segments == True:
            raise Exception("explore_validation_threshold_segments should be called with a list of Participants with require_valid_segments = False")
            
        
        tvalidity = []
        
        for seg in p.segments:
            seglen += seg.completion_time
        segs += len(p.segments)

                       
        for tresh in time_gap_list:     ##time-gap
            invc = 0
            invsegs=[]
            for seg in p.segments:
                if seg.calc_validity2(tresh) == False:
                    invc +=1

            if len(invsegs)>0:
                print("seg:",invsegs)
                    
            tvalidity.append((tresh, invc))
        participants.append( (p.pid,tvalidity, len(p.segments) ) )
        print ( (tvalidity, len(p.segments)) )
       
    print("average seg len",seglen/float(segs))
    return participants


def explore_validation_proportion_threshold_participants(participant_list, include_restored_samples =True, prune_length = None,
                   auto_partition_low_quality_segments = False):
    """Explores different threshiold values for the proportion of valid samples method for evaluating the validity of each Particiapnt in the list
    """
    participants = []
    seglen = 0
    segs = 0
    for p in participant_list:
        print("pid:", p.pid)
        tvalidity = []
            
        for seg in p.segments:
            seglen += seg.completion_time
        segs += len(p.segments)
        
        if include_restored_samples == False:
            for tresh in range(1,102,1):    ##proportion 
                invc = 0
                if p.is_valid(method=1, threshold = tresh/100.0) == False:
                    invc +=1                        
                tvalidity.append((tresh, invc))
        else:
            for tresh in range(1,102,1):    ##proportion Fixation
                invc = 0
                if p.is_valid(method=3, threshold = tresh/100.0) == False:
                    invc +=1                        
                tvalidity.append((tresh, invc))

        participants.append( (p.pid,tvalidity, len(p.segments) ) )
        print ( (tvalidity, len(p.segments)) )
                 
    return participants

def output_Validity_info_Participants(user_list, include_restored_samples, auto_partition_low_quality_segments_flag):
    """ Outputs the Validuty info for Participants for different Threshold values
    """
    pv = explore_validation_proportion_threshold_participants(participant_list=user_list, include_restored_samples = include_restored_samples, prune_length = None, 
                        auto_partition_low_quality_segments = auto_partition_low_quality_segments_flag)
    
    for rate in range(1,102,1): ##porportion
        usr=[]
        totalseg = 0
        inv_user = 0
        for p in pv:
            pid, i,t = p
            totalseg += t
            _,invc = i[rate-1] 
            if invc > 0 :
                inv_user+=1
                usr.append(invc)
            else:
                usr.append(0)
            
    #    print rate*100,":",inv_seg,"/",totalseg,"user:",inv_user,":",usr
        print(rate,": users with invalid Segment:",inv_user,":",usr)
    print()
    print("Total Segments:",totalseg)
##########


def output_Validity_info_Segments(user_list, auto_partition_low_quality_segments_flag, validity_method, threshold_gaps_list = [], output_file= None):
    """ Outputs the Validuty info for Segments over all Participants for different Threshold values
    """
    if output_file:
        print("writing results to: " + output_file)
        ofile = open(output_file,"w")
        s="Threshold,inv_seg,totalseg,# of Participants with invalid Segment,# of invalid Segements for each Participant"+"\n"
        ofile.write(s)
        print()
        if validity_method == 1|validity_method == 3:   ##porportion
            pv = explore_validation_proportion_threshold_segments(participant_list=user_list, prune_length = None,
                               auto_partition_low_quality_segments = auto_partition_low_quality_segments_flag)
            for rate in range(1,102,1): 
                usr=[]
                totalseg = 0
                inv_seg = 0
                inv_user = 0
                for p in pv:
                    pid, i,t = p
                    totalseg += t
                    _,invc = i[rate-1] 
                    inv_seg += invc
                    if invc > 0 :
                        inv_user+=1
                        usr.append(invc)
                    else:
                        usr.append(0)
                print("writin:"+str(rate))
                s= str(rate),","+str(inv_seg),","+str(totalseg)+","+str(inv_user)+","+str(usr)+"\n"
                ofile.write(s)
    
        elif validity_method == 2:  ##time gap\
            pv = explore_validation_time_gap_threshold_segments(participant_list = user_list, time_gap_list = threshold_gaps_list, prune_length = None, 
                                                                auto_partition_low_quality_segments = auto_partition_low_quality_segments_flag)
            for gap_index in range(len(threshold_gaps_list)): 
                usr=[]
                totalseg = 0
                inv_seg = 0
                inv_user = 0
                for p in pv:
                    pid, i,t = p
                    totalseg += t
                    _,invc = i[gap_index]    #rate-1 
                    inv_seg += invc
                    if invc > 0 :
                        inv_user+=1
                        usr.append(invc)
                    else:
                        usr.append(0)
                    
                print("writin:"+str(threshold_gaps_list[gap_index]))
                s = str(threshold_gaps_list[gap_index])+","+str(inv_seg)+","+str(totalseg)+","+str(inv_user)+","+str(usr)+"\n"
                ofile.write(s)
        print("Finished writing to file")
        ofile.close()
    else:    
        print
        if validity_method == 1|validity_method == 3:   ##porportion
            pv = explore_validation_proportion_threshold_segments(participant_list=user_list, prune_length = None,
                               auto_partition_low_quality_segments = auto_partition_low_quality_segments_flag)
            for rate in range(1,102,1): 
                usr=[]
                totalseg = 0
                inv_seg = 0
                inv_user = 0
                for p in pv:
                    pid, i,t = p
                    totalseg += t
                    _,invc = i[rate-1] 
                    inv_seg += invc
                    if invc > 0 :
                        inv_user+=1
                        usr.append(invc)
                    else:
                        usr.append(0)
                    
                print(rate,":",inv_seg,"/",totalseg,", users with invalid Segment::",inv_user,":",usr)
    
        elif validity_method == 2:  ##time gap\
            pv = explore_validation_time_gap_threshold_segments(participant_list = user_list, time_gap_list = threshold_gaps_list, prune_length = None, 
                                                                auto_partition_low_quality_segments = auto_partition_low_quality_segments_flag)
            for gap_index in range(len(threshold_gaps_list)): 
                usr=[]
                totalseg = 0
                inv_seg = 0
                inv_user = 0
                for p in pv:
                    pid, i,t = p
                    totalseg += t
                    _,invc = i[gap_index]    #rate-1 
                    inv_seg += invc
                    if invc > 0 :
                        inv_user+=1
                        usr.append(invc)
                    else:
                        usr.append(0)
                    
                print(threshold_gaps_list[gap_index],":",inv_seg,"/",totalseg,", users with invalid Segment:",inv_user,":",usr)        
##################



########### PRINT scence validity
#print
#actionids = [1    ,2    ,3    ,4    ,9    ,10    ,11]
#print '\t',repr(actionids).strip('[').rstrip(']').replace(',','\t')
#for p in ps:
#    validscs = map(lambda x:x.scid, filter(lambda x:x.is_valid,p.scenes))
#    output = map(lambda x:int(x in validscs),actionids)
#    print p.id,'\t',(repr(output)).strip('[').rstrip(']').replace(',','\t')
#print
#for p in ps:
#    existingscs = filter(lambda x:x.scid in actionids,p.scenes)
#    exscdic = {}
#    for sc in existingscs:
#        exscdic[sc.scid] = sc
#        
#    def retnumberofsegs(dic,acid):
#        if acid in dic.keys():
#            return dic[acid].features['numsegments']
#        else:
#            return 0
#    output = map(lambda x:retnumberofsegs(exscdic,x),actionids)
#    print p.id,'\t',(repr(output)).strip('[').rstrip(']').replace(',','\t')    


###### PRINT invalid segements 
#for p in ps:
#    ##p.print_()
#    print p.id
#    print p.invalid_segments()
#    print p.valid_segments() 
    
def output_percent_discarded(participant_list, output_file= None):
    """percent of data Discarded due to validity
    """
    if output_file:
        print("writing results to: "+output_file)
        ofile = open(output_file,"w")
        s="pid,is_valid,valid_duration,total_duration,valid_portion"+"\n"
        ofile.write(s)
        for p in participant_list:
            if p.require_valid_segments == True:
                raise Exception("output_percent_discarded should be called with a list of Participants with require_valid_segments = False")

            vlength_sum = sum(map (lambda y:y.length,filter(lambda x:x.is_valid,p.segments)))
            length_sum = sum(map(lambda x:x.length,p.segments))
            s=str(p.pid)+","+str(p.is_valid())+","+str(vlength_sum)+","+str(length_sum)+","+str(vlength_sum*1.0/length_sum)+"\n"
            ofile.write(s)
        ofile.close()
    else:
        print("pid,is_valid,valid_duration,total_duration,valid_portion")
        for p in participant_list:
            vlength_sum = sum(map (lambda y:y.length,filter(lambda x:x.is_valid,p.segments)))
            length_sum = sum(map(lambda x:x.length,p.segments))
            print(p.pid,p.is_valid(),vlength_sum,length_sum,vlength_sum*1.0/length_sum)
        
    ###### 
