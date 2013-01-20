'''
Created on 20 Jan 2013

@author: bruno
'''
import load_data
import spam

class StatsGenerator:
    def __init__(self):
        pass
    
    def process_message_collection(self, sample_ratio, options=[]):
        data = load_data.Data()
        processor = spam.SpamProcessor(options)
        tagmap = {
                  'ham': 'Good',
                  'spam': 'Bad'
                  }
        sample_len = sample_ratio * len(data.all_msg)
        matches = []
        false_positives = []
        false_negatives = []
        neutrals = []
        unexpected_mismatches = []
        for idx, d in enumerate(data.all_msg):
            msg = d[0]
            tag = d[1]
            if idx < sample_len:
                if tag == 'ham':
                    processor.flag_as_good(msg)
                elif tag == 'spam':
                    processor.flag_as_bad(msg)
                else:
                    self.fail("Unexpected tag {0} in message list".format(tag))
            else:
                expected_score_tag = tagmap[tag]
                score = processor.score(msg)
                actual_score_tag = score[1]
                if expected_score_tag == actual_score_tag:
                    matches.append((d, score))
                elif expected_score_tag == 'Good' and actual_score_tag == 'Bad':
                    false_positives.append((d, score))
                elif expected_score_tag == 'Bad' and actual_score_tag == 'Good':
                    false_negatives.append((d, score))
                elif actual_score_tag == 'Neutral':
                    neutrals.append((d, score))
                else:
                    unexpected_mismatches.append((d, score))
        total = len(matches) + len(false_positives) + len(false_negatives) + len(neutrals) + len(unexpected_mismatches)
        return {
                'total': total,
                'matches': self.list_stats(matches, total),
                'false_positives': self.list_stats(false_positives, total, len(matches)),
                'false_negatives': self.list_stats(false_negatives, total, len(matches)),
                'neutrals': self.list_stats(neutrals, total),
                'unexpected_mismatches': self.list_stats(unexpected_mismatches, total)
                }

    def list_stats(self, lst, total, matches = None):
        if matches is None:
            return (len(lst), float(len(lst)/float(total)))
        else:
            return (len(lst), float(len(lst)/float(total)), float(len(lst)/float(matches)))

if __name__ == '__main__':
    import argparse
    import json
    arg_parser = argparse.ArgumentParser(description='Generate spam filter stats.')
    arg_parser.add_argument('--json', '-j', action='store_true')
    arg_parser.add_argument('--csv', '-c', action='store_true')
    args = arg_parser.parse_args()
    
    stats_gen = StatsGenerator()
    runs = [
            {
             'sample_ratio': 0.05,
             'options': []
             },
            {
             'sample_ratio': 0.05,
             'options': ['pairs']
             },
            {
             'sample_ratio': 0.05,
             'options': ['lower']
             },
            {
             'sample_ratio': 0.05,
             'options': ['pairs', 'lower']
             }
            ]
    results = [{
                'run': r,
                'result': stats_gen.process_message_collection(r['sample_ratio'], r['options'])
                }
               for r in runs
               ]
    if args.json:
        print json.dumps(results)
    elif args.csv:
        print "Run,Matches,Neutrals,False positives,False negatives"
        for rs in results:
            run = rs['run']
            result = rs['result']
            run_cell = '"{0};{1}"'.format(
                                     run['sample_ratio'],
                                     format(','.join([str(vv) for vv in run['options']])))
            print '{0},{1},{2},{3},{4}'.format(
                                               run_cell,
                                               result['matches'][1],
                                               result['neutrals'][1],
                                               result['false_positives'][1],
                                               result['false_negatives'][1]
                                               )
    else:
        for rs in results:
            r = rs['run']
            result = rs['result']
            r_out = {}
            for k, v in result.iteritems():
                if k == 'total':
                    r_out[k] = v
                else:
                    r_out[k] = [v[0]] + ["{0:.2f}".format(100*vv) for vv in v[1:]]
            print "Run: {0}\nResult: {1}\n".format(r, r_out)