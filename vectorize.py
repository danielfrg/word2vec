import word2vec
import sys
import csv

from numpy import ndarray, append

csv.field_size_limit(sys.maxsize)

vsize = 100

csvin = sys.argv[1]
csvtmp = csvin+".tmp"
csvbin = csvin+".bin"
csvout = csvin+".vec"#"/dev/stdout" 
col = int(sys.argv[2])
mcol = 4

def concatvect(events, model, size):
  i = len(events)-1
  r = ndarray([])


  while size<>0:
    assert(i>0)
    event = events[i]
    #print event, size, i
    try:

      #if event in model:
      r = append(r,model[event])
      size = size - 1
    
    except KeyError:
      pass
      #print "pass"
    
    i = i - 1
  
  #print size
  return r  


  """ 
  for i in range(size):
    print events[-i]
  for event in events:
    print event,
    r = append(r,model[event])
  print ""
  return r
  """  

with open(csvin, 'rb') as csvfile_in:
  with open(csvtmp, 'wb') as csvfile_tmp:
    csvfile_in_reader   = csv.reader(csvfile_in, delimiter='\t')
    for row in csvfile_in_reader:
      if len(row) == mcol:
        csvfile_tmp.write(row[col]+"\n")
      
  word2vec.word2vec(csvtmp, csvbin,size=vsize,min_count=1,verbose=True)
  print ""
  model = word2vec.load(csvbin)

with open(csvin, 'rb') as csvfile_in:
  with open(csvout, 'wb') as csvfile_out:
    csvfile_in_reader    = csv.reader(csvfile_in, delimiter='\t')
    csvfile_out_writer   = csv.writer(csvfile_out, delimiter='\t')
    for row in csvfile_in_reader:
      
      if len(row) == mcol:
        last_events = row[col].split("  ")#[-11:-1]
        #print last_events
        floats = list(concatvect(last_events,model,9))
        csvfile_out_writer.writerow(row[0:col]+floats+row[col+1:])

  #for word in model.vocab:
  #  if word <> '</s>':
  #    #print word,
  #    d = model.cosine(word)
  #    for (word, res) in d.items():
  #      print word+":"
  #      for r in res:
  #        print r

      #for f in model[word]:
      #  print f,
      #print ""
